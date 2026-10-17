"""
Lõi AirMouse (không phụ thuộc giao diện).

Đọc chuột / touchpad / bàn phím của laptop và gửi qua Wi-Fi (UDP) sang app AirMouse trên Android.
 - Đẩy chuột chạm mép PHẢI màn hình laptop  -> chuột "nhảy" sang điện thoại
 - Kéo con trỏ trên điện thoại ra mép TRÁI  -> chuột quay lại laptop
 - Alt+M                                    -> chuyển qua lại thủ công (luôn hoạt động)
 - Khi đang điều khiển điện thoại:
     * Gõ ký tự thường -> tự động copy vào Clipboard điện thoại (Remote Typing)
     * Esc -> Back,  Home -> Home

Giao diện (GUI/CLI) chỉ cần tạo `Engine`, truyền vào một hàm `emit(kind, **data)`:
    emit("log",   level="info|ok|warn|error", text=str)
    emit("state", state="stopped|connecting|connected|remote")
    emit("devices", names=[str, ...])
"""
from __future__ import annotations

import base64
import math
import os
import queue
import select
import socket
import threading
import time
from typing import Callable, Optional

from .config import Settings

try:
    import evdev
    from evdev import ecodes as e

    EVDEV_ERROR: Optional[str] = None
except ImportError:  # pragma: no cover - phụ thuộc môi trường
    evdev = None  # type: ignore
    e = None  # type: ignore
    EVDEV_ERROR = "Thiếu thư viện evdev. Chạy: sudo apt install python3-evdev  (hoặc pip install evdev)"

try:
    from pynput import keyboard as kb_listener
except Exception:  # pragma: no cover
    kb_listener = None

SEND_INTERVAL = 0.008        # gộp tối đa ~125 gói/giây
PING_FAST = 1.5              # chu kỳ PING khi chưa kết nối (giây)
PING_SLOW = 4.0              # chu kỳ PING khi đã kết nối
LINK_TIMEOUT = 11.0          # quá thời gian này không nghe phản hồi -> coi là mất kết nối

STOPPED, CONNECTING, CONNECTED, REMOTE = "stopped", "connecting", "connected", "remote"

Emit = Callable[..., None]


def _noop(*_a, **_k) -> None:
    pass


if e is not None:
    BUTTONS = {e.BTN_LEFT: "L", e.BTN_RIGHT: "R", e.BTN_MIDDLE: "M"}
    TOOLS = {e.BTN_TOOL_FINGER: 1, e.BTN_TOOL_DOUBLETAP: 2, e.BTN_TOOL_TRIPLETAP: 3}

    # Mapping cơ bản từ evdev keycode sang ký tự (US Layout)
    _CHAR_MAP = {
        e.KEY_A: 'a', e.KEY_B: 'b', e.KEY_C: 'c', e.KEY_D: 'd', e.KEY_E: 'e',
        e.KEY_F: 'f', e.KEY_G: 'g', e.KEY_H: 'h', e.KEY_I: 'i', e.KEY_J: 'j',
        e.KEY_K: 'k', e.KEY_L: 'l', e.KEY_M: 'm', e.KEY_N: 'n', e.KEY_O: 'o',
        e.KEY_P: 'p', e.KEY_Q: 'q', e.KEY_R: 'r', e.KEY_S: 's', e.KEY_T: 't',
        e.KEY_U: 'u', e.KEY_V: 'v', e.KEY_W: 'w', e.KEY_X: 'x', e.KEY_Y: 'y',
        e.KEY_Z: 'z',
        e.KEY_1: '1', e.KEY_2: '2', e.KEY_3: '3', e.KEY_4: '4', e.KEY_5: '5',
        e.KEY_6: '6', e.KEY_7: '7', e.KEY_8: '8', e.KEY_9: '9', e.KEY_0: '0',
        e.KEY_SPACE: ' ', e.KEY_ENTER: '\n', e.KEY_BACKSPACE: '\b',
        e.KEY_DOT: '.', e.KEY_COMMA: ',', e.KEY_SLASH: '/', e.KEY_MINUS: '-',
        e.KEY_EQUAL: '=', e.KEY_SEMICOLON: ';', e.KEY_APOSTROPHE: "'",
        e.KEY_LEFTBRACE: '[', e.KEY_RIGHTBRACE: ']', e.KEY_BACKSLASH: '\\',
    }

    _SHIFT_MAP = {
        '1': '!', '2': '@', '3': '#', '4': '$', '5': '%', '6': '^', '7': '&',
        '8': '*', '9': '(', '0': ')', '-': '_', '=': '+', '[': '{', ']': '}',
        '\\': '|', ';': ':', "'": '"', ',': '<', '.': '>', '/': '?', '`': '~',
    }
else:  # pragma: no cover
    BUTTONS, TOOLS = {}, {}
    _CHAR_MAP, _SHIFT_MAP = {}, {}


class Dev:
    """Trạng thái của một thiết bị chuột hoặc touchpad."""

    def __init__(self, dev):
        self.dev = dev
        caps = dev.capabilities()
        self.is_pad = e.EV_REL not in caps
        self.dx = 0.0
        self.dy = 0.0
        self.scroll = 0.0
        # chỉ dùng cho touchpad
        self.last = [None, None]
        self.touching = False
        self.fingers = 0
        self.max_fingers = 0
        self.touch_t = 0.0
        self.travel = 0.0
        self.rng = [1, 1]
        if self.is_pad:
            info = {code: i for code, i in caps[e.EV_ABS]}
            self.rng = [
                max(1, info[e.ABS_X].max - info[e.ABS_X].min),
                max(1, info[e.ABS_Y].max - info[e.ABS_Y].min),
            ]


def find_devices():
    """Trả về (danh sách chuột/touchpad, danh sách bàn phím)."""
    mice, keyboards = [], []
    for path in evdev.list_devices():
        try:
            d = evdev.InputDevice(path)
        except OSError:
            continue
        caps = d.capabilities()
        keys = caps.get(e.EV_KEY, [])
        rel = caps.get(e.EV_REL, [])
        abs_codes = [c for c, _ in caps.get(e.EV_ABS, [])]
        if e.REL_X in rel and e.BTN_LEFT in keys:
            mice.append(Dev(d))
        elif e.ABS_X in abs_codes and e.BTN_TOUCH in keys and e.BTN_LEFT in keys:
            mice.append(Dev(d))  # touchpad
        elif e.KEY_LEFTCTRL in keys and e.KEY_M in keys:
            keyboards.append(d)
    return mice, keyboards


def get_screen_size():
    try:
        import tkinter

        r = tkinter.Tk()
        r.withdraw()
        w, h = r.winfo_screenwidth(), r.winfo_screenheight()
        r.destroy()
        return w, h
    except Exception:
        return None


class Bridge:
    """Logic chuyển đổi laptop <-> điện thoại và đóng gói lệnh UDP."""

    def __init__(self, cfg: Settings, mice, keyboards, ctl, sw, sh, emit: Emit = _noop):
        self.cfg = cfg
        self.emit = emit
        self.mice = mice
        self.keyboards = keyboards
        self.ctl = ctl  # pynput Controller (X11) hoặc None
        self.sw, self.sh = sw, sh
        self.remote = False
        self.connected = False
        self.push = 0.0
        self.vx, self.vy = sw / 2, sh / 2  # vị trí ước lượng (chế độ blind)
        self.pend_dx = self.pend_dy = 0.0
        self.last_send = 0.0
        self.last_ping = 0.0
        self.last_pong = 0.0
        self.held = set()
        self.held_buttons = {}
        self.drag_start_time = 0.0
        self.drag_total_dist = 0.0

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", cfg.listen_port))
        self.addr = (cfg.phone, cfg.port)

        # trạng thái bàn phím từ xa
        self.type_buffer = []
        self.last_type_time = 0.0
        self.modifiers = {"shift": False, "ctrl": False, "alt": False}

        self._wake_r, self._wake_w = os.pipe()
        os.set_blocking(self._wake_r, False)
        self.requests: "queue.Queue[str]" = queue.Queue()
        self._stop = False

    # ---------- tiện ích ----------
    def log(self, text: str, level: str = "info") -> None:
        self.emit("log", level=level, text=text)

    @property
    def state(self) -> str:
        if self.remote:
            return REMOTE
        return CONNECTED if self.connected else CONNECTING

    def _publish_state(self) -> None:
        self.emit("state", state=self.state)

    def request(self, what: str) -> None:
        """Gọi từ thread khác: 'toggle' | 'stop'."""
        self.requests.put(what)
        try:
            os.write(self._wake_w, b"x")
        except OSError:
            pass

    def close(self) -> None:
        for fd in (self._wake_r, self._wake_w):
            try:
                os.close(fd)
            except OSError:
                pass
        try:
            self.sock.close()
        except OSError:
            pass

    # ---------- mạng ----------
    def send(self, cmd: str) -> None:
        try:
            self.sock.sendto(f"{self.cfg.secret}|{cmd}".encode(), self.addr)
        except OSError as ex:
            self.log(f"Lỗi gửi: {ex}", "error")

    def flush_pending(self, force: bool = False) -> None:
        if not (self.pend_dx or self.pend_dy):
            return
        now = time.time()
        if not force and now - self.last_send < SEND_INTERVAL:
            return
        self.send(f"MOVE {self.pend_dx:.1f} {self.pend_dy:.1f}")
        self.pend_dx = self.pend_dy = 0.0
        self.last_send = now

    def on_socket(self) -> None:
        data, _ = self.sock.recvfrom(512)
        text = data.decode(errors="ignore")
        secret, _, cmd = text.partition("|")
        if secret != self.cfg.secret:
            return
        cmd = cmd.strip()
        self.last_pong = time.time()
        if cmd == "PONG":
            if not self.connected:
                self.connected = True
                self.log("Đã kết nối với điện thoại.", "ok")
                self._publish_state()
        elif cmd.startswith("RETURN") and self.remote:
            try:
                ratio = float(cmd.split()[1])
            except (IndexError, ValueError):
                ratio = 0.5
            self.leave_remote(ratio=ratio, notify=False)

    def tick_link(self) -> None:
        """Gửi PING định kỳ và phát hiện mất kết nối."""
        now = time.time()
        interval = PING_SLOW if self.connected else PING_FAST
        if now - self.last_ping >= interval:
            self.last_ping = now
            self.send("PING")
        if self.connected and now - self.last_pong > LINK_TIMEOUT:
            self.connected = False
            self.log("Mất kết nối với điện thoại — đang thử lại…", "warn")
            self._publish_state()

    # ---------- chuyển đổi laptop <-> điện thoại ----------
    def position(self):
        if not self.ctl:
            return None
        try:
            return self.ctl.position
        except Exception:
            return None

    def enter_remote(self, ratio: float = 0.5) -> None:
        if self.remote:
            return
        for d in self.mice:
            try:
                d.dev.grab()
            except OSError as ex:
                self.log(f"Không grab được {d.dev.name}: {ex}", "warn")
            d.dx = d.dy = d.scroll = 0.0
            d.last = [None, None]
        self.remote = True
        self.push = 0.0
        self.pend_dx = self.pend_dy = 0.0
        self.send(f"ENTER {min(max(ratio, 0.0), 1.0):.4f}")
        self.log("Đang điều khiển ĐIỆN THOẠI  (Alt+M để quay lại)", "ok")
        self._publish_state()

    def leave_remote(self, ratio: Optional[float] = None, notify: bool = True) -> None:
        if not self.remote:
            return
        self.flush_pending(force=True)
        for d in self.mice:
            try:
                d.dev.ungrab()
            except OSError:
                pass
            d.last = [None, None]
            d.touching = False
        self.remote = False
        self.push = 0.0
        if notify:
            self.send("LEAVE")
        if ratio is not None:
            if self.ctl:
                try:
                    self.ctl.position = (self.sw - 4, int(ratio * self.sh))
                except Exception:
                    pass
            self.vx, self.vy = self.sw - 100, ratio * self.sh
        self.log("Đã quay về LAPTOP", "info")
        self._publish_state()

    def toggle_remote(self) -> None:
        if self.remote:
            self.leave_remote(ratio=None, notify=True)
        else:
            self.enter_remote(0.5)

    def check_edge(self, dx: float, dy: float) -> None:
        if not self.cfg.edge_enabled:
            return
        if self.ctl:  # X11: biết vị trí thật của con trỏ
            pos = self.position()
            if pos is None:
                return
            if pos[0] >= self.sw - 2 and dx > 0:
                self.push += dx
                if self.push >= self.cfg.edge_push:
                    self.enter_remote(pos[1] / self.sh)
            else:
                self.push = 0.0
        elif self.cfg.blind_edge:  # Wayland: chỉ ước lượng
            self.vy = min(max(self.vy + dy, 0), self.sh)
            nx = self.vx + dx
            if nx > self.sw:
                self.push += nx - self.sw
                self.vx = self.sw
                if self.push >= self.cfg.edge_push * 5:
                    self.enter_remote(self.vy / self.sh)
            else:
                self.vx = max(nx, 0)
                self.push = 0.0

    # ---------- xử lý sự kiện ----------
    def on_scroll(self, v: float) -> None:
        if not self.remote or not v:
            return
        self.flush_pending(force=True)
        if self.modifiers.get("ctrl", False):
            self.send(f"HSCROLL {v:.2f}")
        else:
            self.send(f"SCROLL {v:.2f}")

    def on_button(self, name: str, value: int) -> None:
        if self.remote and value in (0, 1):
            self.flush_pending(force=True)

            if value == 1:
                self.held_buttons[name] = True
            else:
                self.held_buttons.pop(name, None)

            if name == "L":
                if value == 1:
                    self.drag_start_time = time.time()
                    self.drag_total_dist = 0.0
                else:
                    dur_ms = int((time.time() - (self.drag_start_time or time.time())) * 1000)
                    self.send(f"BTN L {value} {dur_ms} {self.drag_total_dist:.1f}")
                    return

            self.send(f"BTN {name} {value}")

    # ---------- Bàn phím từ xa ----------
    def flush_type_buffer(self) -> None:
        """Gửi chuỗi ký tự đã gom được sang Android dưới dạng CLIP (base64)."""
        if not self.type_buffer:
            return
        text = "".join(self.type_buffer)
        self.type_buffer.clear()
        encoded = base64.b64encode(text.encode("utf-8")).decode("ascii")
        self.send(f"CLIP {encoded}")
        self.log(f"[DEBUG] FLUSH -> Gửi CLIP: “{text}”", "ok")

    def handle_key_event(self, key, pressed: bool) -> bool:
        """Xử lý sự kiện phím (từ pynput).
        
        ĐÃ VÔ HIỆU HÓA: Logic chính đã chuyển sang on_keyboard() sử dụng evdev 
        để tương thích hoàn hảo với Wayland và tránh xung đột input grab.
        Hàm này giữ lại interface nhưng luôn trả về False.
        """
        return False

    def click(self, name: str) -> None:
        self.on_button(name, 1)
        self.on_button(name, 0)

    def pad_abs(self, d: Dev, ev) -> None:
        if ev.code == e.ABS_X:
            axis = 0
        elif ev.code == e.ABS_Y:
            axis = 1
        else:
            return
        if d.touching and d.last[axis] is not None:
            norm = (ev.value - d.last[axis]) / d.rng[axis]
            d.travel += abs(norm)
            if d.fingers >= 2:
                if axis == 1:
                    d.scroll += -norm * 6.0  # cuộn tự nhiên
            else:
                delta = norm * 1800 * self.cfg.speed
                if axis == 0:
                    d.dx += delta
                else:
                    d.dy += delta
        d.last[axis] = ev.value

    def pad_key(self, d: Dev, ev) -> None:
        if ev.code in TOOLS:
            if ev.value:
                d.fingers = TOOLS[ev.code]
                d.max_fingers = max(d.max_fingers, d.fingers)
            elif d.fingers == TOOLS[ev.code]:
                d.fingers = 0
            d.last = [None, None]
        elif ev.code == e.BTN_TOUCH:
            if ev.value:
                d.touching = True
                d.touch_t = time.time()
                d.travel = 0.0
                d.max_fingers = 0
            else:
                d.touching = False
                d.last = [None, None]
                quick = time.time() - d.touch_t < 0.22 and d.travel < 0.02
                if self.remote and quick:  # chạm nhanh = click
                    if d.max_fingers <= 1:
                        self.click("L")
                    elif d.max_fingers == 2:
                        self.click("R")

    def flush_motion(self, d: Dev) -> None:
        if d.scroll:
            self.on_scroll(d.scroll)
            d.scroll = 0.0
        dx, dy = d.dx, d.dy
        d.dx = d.dy = 0.0
        if not (dx or dy):
            return

        # đang kéo (giữ chuột trái): cộng dồn quãng đường thực tế
        if self.remote and self.held_buttons.get("L", False):
            self.drag_total_dist += math.hypot(dx, dy)

        if self.remote:
            self.pend_dx += dx
            self.pend_dy += dy
        else:
            self.check_edge(dx, dy)

    def on_input(self, d: Dev, ev) -> None:
        if ev.type == e.EV_REL and not d.is_pad:
            if ev.code == e.REL_X:
                d.dx += ev.value * self.cfg.speed
            elif ev.code == e.REL_Y:
                d.dy += ev.value * self.cfg.speed
            elif ev.code == e.REL_WHEEL:
                self.on_scroll(-ev.value)
        elif ev.type == e.EV_ABS and d.is_pad:
            self.pad_abs(d, ev)
        elif ev.type == e.EV_KEY:
            if ev.code in BUTTONS:
                self.on_button(BUTTONS[ev.code], ev.value)
            elif d.is_pad:
                self.pad_key(d, ev)
        elif ev.type == e.EV_SYN and ev.code == e.SYN_REPORT:
            self.flush_motion(d)

    def on_keyboard(self, ev) -> None:
        if ev.type != e.EV_KEY:
            return
        
        # Cập nhật trạng thái phím đang giữ
        if ev.value:
            self.held.add(ev.code)
        else:
            self.held.discard(ev.code)

        # 1. Xử lý Hotkey Alt+M (Toggle Remote)
        alt = e.KEY_LEFTALT in self.held or e.KEY_RIGHTALT in self.held
        if ev.code == e.KEY_M and ev.value == 1 and alt:
            self.toggle_remote()
            return

        # 2. Xử lý Remote Typing (chỉ khi đang remote)
        if not self.remote:
            return

        # Bỏ qua nếu không phải press (value=1) hoặc repeat (value=2)
        if ev.value != 1:
            return

        # Kiểm tra Shift/CapsLock
        shift_pressed = e.KEY_LEFTSHIFT in self.held or e.KEY_RIGHTSHIFT in self.held
        
        char = None
        if ev.code in _CHAR_MAP:
            base_char = _CHAR_MAP[ev.code]
            if shift_pressed and base_char in _SHIFT_MAP:
                char = _SHIFT_MAP[base_char]
            elif shift_pressed and base_char.isalpha():
                char = base_char.upper()
            else:
                char = base_char
        
        if char:
            now = time.time()
            if self.type_buffer and now - self.last_type_time > 0.5:
                self.flush_type_buffer()
            self.last_type_time = now
            
            # Handle special keys explicitly if needed, otherwise append to buffer
            if char == '\n':
                self.flush_type_buffer()
                self.send("KEY ENTER")
            elif char == '\b':
                self.flush_type_buffer()
                self.send("KEY BACKSPACE")
            else:
                self.type_buffer.append(char)

    # ---------- vòng lặp chính ----------
    def _drain_requests(self) -> None:
        try:
            os.read(self._wake_r, 64)
        except OSError:
            pass
        while True:
            try:
                what = self.requests.get_nowait()
            except queue.Empty:
                return
            if what == "stop":
                self._stop = True
            elif what == "toggle":
                self.toggle_remote()

    def run(self) -> None:
        sources = {self.sock.fileno(): ("sock", None), self._wake_r: ("wake", None)}
        for d in self.mice:
            sources[d.dev.fd] = ("mouse", d)
        for k in self.keyboards:
            sources[k.fd] = ("kbd", k)
        self._publish_state()
        try:
            while not self._stop:
                self.tick_link()
                pending = bool(self.pend_dx or self.pend_dy)
                try:
                    ready, _, _ = select.select(list(sources), [], [], 0.01 if pending else 0.25)
                except (OSError, ValueError):
                    ready = []
                for fd in ready:
                    kind, obj = sources[fd]
                    try:
                        if kind == "wake":
                            self._drain_requests()
                        elif kind == "sock":
                            self.on_socket()
                        elif kind == "mouse":
                            for ev in obj.dev.read():
                                self.on_input(obj, ev)
                        else:
                            for ev in obj.read():
                                self.on_keyboard(ev)
                    except BlockingIOError:
                        pass
                    except OSError:
                        if kind in ("mouse", "kbd"):
                            self.log("Thiết bị bị rút ra, bỏ qua.", "warn")
                            sources.pop(fd, None)
                if self.remote:
                    self.flush_pending()
        finally:
            self.leave_remote(ratio=None, notify=True)
            self.close()


class Engine:
    """Khởi tạo thiết bị, chạy Bridge trên thread riêng — dùng chung cho GUI và CLI."""

    def __init__(self, cfg: Settings, emit: Emit = _noop):
        self.cfg = cfg
        self.emit = emit
        self.bridge: Optional[Bridge] = None
        self.thread: Optional[threading.Thread] = None
        self._kbd = None

    @property
    def running(self) -> bool:
        return bool(self.thread and self.thread.is_alive())

    def _log(self, text: str, level: str = "info") -> None:
        self.emit("log", level=level, text=text)

    def start(self) -> bool:
        if self.running:
            return True
        if EVDEV_ERROR:
            self._log(EVDEV_ERROR, "error")
            return False

        mice, keyboards = find_devices()
        if not mice:
            self._log(
                "Không tìm thấy chuột/touchpad (hoặc chưa có quyền đọc /dev/input). "
                "Chạy: sudo usermod -aG input $USER rồi đăng xuất/đăng nhập lại.",
                "error",
            )
            return False
        self.emit("devices", names=[d.dev.name for d in mice])
        self._log("Thiết bị chuột: " + ", ".join(d.dev.name for d in mice))
        if not keyboards:
            self._log("Không đọc được bàn phím → phím tắt Alt+M không dùng được.", "warn")

        cfg = self.cfg
        size = None
        if not (cfg.screen_width and cfg.screen_height):
            size = get_screen_size()
        sw = cfg.screen_width or (size[0] if size else 1920)
        sh = cfg.screen_height or (size[1] if size else 1080)
        if not (cfg.screen_width and cfg.screen_height) and not size:
            self._log("Không đọc được kích thước màn hình, dùng 1920×1080 (chỉnh bằng --screen-width/--screen-height).", "warn")

        ctl = None
        wayland = os.environ.get("XDG_SESSION_TYPE", "").lower() == "wayland"
        if not wayland and cfg.edge_enabled:
            try:
                from pynput.mouse import Controller

                ctl = Controller()
                _ = ctl.position
            except Exception as ex:
                self._log(f"Không dùng được pynput ({ex}) → không phát hiện được mép màn hình.", "warn")
                ctl = None
        if not cfg.edge_enabled:
            self._log("Chuyển bằng mép: TẮT — dùng Alt+M.")
        elif ctl:
            self._log(f"Chuyển bằng mép: BẬT (màn hình {sw}×{sh}). Đẩy chuột sang phải để sang điện thoại.")
        elif cfg.blind_edge:
            self._log("Wayland: chuyển bằng mép theo ước lượng (có thể chuyển nhầm).", "warn")
        else:
            self._log("Wayland: không đọc được vị trí con trỏ → dùng Alt+M (hoặc bật “Mép ước lượng”).", "warn")

        try:
            bridge = Bridge(cfg, mice, keyboards, ctl, sw, sh, self.emit)
        except OSError as ex:
            self._log(f"Không mở được cổng UDP {cfg.listen_port}: {ex}", "error")
            return False
        self.bridge = bridge

        self._start_keyboard(bridge)

        self.thread = threading.Thread(target=self._run, name="airmouse-bridge", daemon=True)
        self.thread.start()
        self._log(f"Đang kết nối tới {cfg.phone}:{cfg.port}…")
        return True

    def _start_keyboard(self, bridge: Bridge) -> None:
        if not kb_listener:
            self._log("Thiếu 'pynput' → tính năng gõ phím từ xa sẽ không hoạt động.", "warn")
            return
        try:
            self._kbd = kb_listener.Listener(
                on_press=lambda k: bridge.handle_key_event(k, True),
                on_release=lambda k: bridge.handle_key_event(k, False),
            )
            self._kbd.start()
            self._log("[DEBUG] Keyboard listener (pynput) đã khởi động thành công.", "ok")
        except Exception as ex:
            self._kbd = None
            self._log(f"[ERROR] Không khởi tạo được bộ nghe bàn phím: {ex} → gõ phím từ xa KHÔNG hoạt động.", "error")

    def _run(self) -> None:
        try:
            assert self.bridge is not None
            self.bridge.run()
        except Exception as ex:  # an toàn: không để thread chết âm thầm
            self._log(f"Lỗi nội bộ: {ex}", "error")
        finally:
            if self._kbd:
                try:
                    self._kbd.stop()
                except Exception:
                    pass
                self._kbd = None
            self.emit("state", state=STOPPED)

    def toggle_remote(self) -> None:
        if self.bridge and self.running:
            self.bridge.request("toggle")

    def stop(self, timeout: float = 2.0) -> None:
        if self.bridge and self.running:
            self.bridge.request("stop")
            if self.thread:
                self.thread.join(timeout)
