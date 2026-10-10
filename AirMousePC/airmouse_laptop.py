#!/usr/bin/env python3
"""
AirMouse - phần chạy trên LAPTOP (Ubuntu).

Đọc chuột / touchpad / bàn phím của laptop và gửi qua Wi-Fi (UDP) sang app AirMouse trên Android.
 - Kéo chuột chạm mép PHẢI màn hình laptop  -> chuột "nhảy" sang điện thoại
 - Kéo con trỏ trên điện thoại ra mép TRÁI   -> chuột quay lại laptop
 - Phím tắt Ctrl+Alt+M                       -> chuyển qua lại thủ công (luôn hoạt động)
 - Khi đang điều khiển điện thoại: 
     * Gõ ký tự thường -> tự động copy vào Clipboard điện thoại (Remote Typing)
     * Esc             -> Back
     * Home            -> Home
 
Cách chạy:  python3 airmouse_laptop.py --phone 192.168.1.50
"""
import argparse
import os
import select
import socket
import sys
import time

try:
    import evdev
    from evdev import ecodes as e
except ImportError:
    sys.exit("Thiếu thư viện evdev. Chạy: sudo apt install python3-evdev")

try:
    from pynput import keyboard as kb_listener
except ImportError:
    kb_listener = None

BUTTONS = {e.BTN_LEFT: "L", e.BTN_RIGHT: "R", e.BTN_MIDDLE: "M"}
TOOLS = {e.BTN_TOOL_FINGER: 1, e.BTN_TOOL_DOUBLETAP: 2, e.BTN_TOOL_TRIPLETAP: 3}
SEND_INTERVAL = 0.008  # gộp tối đa ~125 gói/giây

# Map phím đặc biệt sang hành động Android (GLOBAL_ACTION_*)
ANDROID_NAV_KEYS = {
    '<esc>': 'BACK',
    '<home>': 'HOME',
    '<end>': 'RECENTS', # Approximation
    '<tab>': 'TAB',     # Will handle differently if possible, else ignore
}
# Các phím khác sẽ được coi là text để gửi sang Clipboard


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
    def __init__(self, args, mice, keyboards, ctl, sw, sh):
        self.args = args
        self.mice = mice
        self.keyboards = keyboards
        self.ctl = ctl            # pynput Controller (X11) hoặc None
        self.sw, self.sh = sw, sh
        self.remote = False
        self.push = 0.0
        self.vx, self.vy = sw / 2, sh / 2   # vị trí ước lượng (chế độ blind)
        self.pend_dx = self.pend_dy = 0.0
        self.last_send = 0.0
        self.held = set()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", args.listen_port))
        self.addr = (args.phone, args.port)
        
        # Keyboard state
        self.type_buffer = []
        self.last_type_time = 0.0
        self.modifiers = {'shift': False, 'ctrl': False, 'alt': False}

    # ---------- mạng ----------
    def send(self, cmd):
        try:
            self.sock.sendto(f"{self.args.secret}|{cmd}".encode(), self.addr)
        except OSError as ex:
            print("Lỗi gửi:", ex)

    def flush_pending(self, force=False):
        if not (self.pend_dx or self.pend_dy):
            return
        now = time.time()
        if not force and now - self.last_send < SEND_INTERVAL:
            return
        self.send(f"MOVE {self.pend_dx:.1f} {self.pend_dy:.1f}")
        self.pend_dx = self.pend_dy = 0.0
        self.last_send = now

    def on_socket(self):
        data, _ = self.sock.recvfrom(512)
        text = data.decode(errors="ignore")
        secret, _, cmd = text.partition("|")
        if secret != self.args.secret:
            return
        cmd = cmd.strip()
        if cmd == "PONG":
            print("✔ Đã kết nối với điện thoại.")
        elif cmd.startswith("RETURN") and self.remote:
            try:
                ratio = float(cmd.split()[1])
            except (IndexError, ValueError):
                ratio = 0.5
            self.leave_remote(ratio=ratio, notify=False)

    # ---------- chuyển đổi laptop <-> điện thoại ----------
    def position(self):
        if not self.ctl:
            return None
        try:
            return self.ctl.position
        except Exception:
            return None

    def enter_remote(self, ratio=0.5):
        if self.remote:
            return
        for d in self.mice:
            try:
                d.dev.grab()
            except OSError as ex:
                print(f"Không grab được {d.dev.name}: {ex}")
            d.dx = d.dy = d.scroll = 0.0
            d.last = [None, None]
        self.remote = True
        self.push = 0.0
        self.pend_dx = self.pend_dy = 0.0
        self.send(f"ENTER {min(max(ratio, 0.0), 1.0):.4f}")
        print("→ Đang điều khiển ĐIỆN THOẠI  (Ctrl+Alt+M để quay lại)")

    def leave_remote(self, ratio=None, notify=True):
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
        print("← Đã quay về LAPTOP")

    def check_edge(self, dx, dy):
        if self.args.no_edge:
            return
        if self.ctl:  # X11: biết vị trí thật của con trỏ
            pos = self.position()
            if pos is None:
                return
            if pos[0] >= self.sw - 2 and dx > 0:
                self.push += dx
                if self.push >= self.args.edge_push:
                    self.enter_remote(pos[1] / self.sh)
            else:
                self.push = 0.0
        elif self.args.blind_edge:  # Wayland: chỉ ước lượng
            self.vy = min(max(self.vy + dy, 0), self.sh)
            nx = self.vx + dx
            if nx > self.sw:
                self.push += nx - self.sw
                self.vx = self.sw
                if self.push >= self.args.edge_push * 5:
                    self.enter_remote(self.vy / self.sh)
            else:
                self.vx = max(nx, 0)
                self.push = 0.0

    # ---------- xử lý sự kiện ----------
    def on_scroll(self, v):
        if not self.remote or not v:
            return
        self.flush_pending(force=True)
        # Kiểm tra xem Ctrl có đang được giữ không (dựa vào modifier state từ keyboard listener)
        if getattr(self, 'modifiers', {}).get('ctrl', False):
            self.send(f"HSCROLL {v:.2f}")
        else:
            self.send(f"SCROLL {v:.2f}")

    def on_button(self, name, value):
        if not hasattr(self, 'held_buttons'):
            self.held_buttons = {}
            
        if self.remote and value in (0, 1):
            self.flush_pending(force=True)
            
            # Cập nhật trạng thái giữ nút
            if value == 1:
                self.held_buttons[name] = True
            else:
                self.held_buttons.pop(name, None)

            if name == "L":
                if value == 1: # Pressed
                    self.drag_start_time = time.time()
                    self.drag_total_dist = 0.0
                else: # Released
                    dur_ms = int((time.time() - getattr(self, 'drag_start_time', time.time())) * 1000)
                    dist = getattr(self, 'drag_total_dist', 0.0)
                    self.send(f"BTN L {value} {dur_ms} {dist:.1f}")
                    return
                    
            self.send(f"BTN {name} {value}")

    # ---------- Bàn phím từ xa ----------
    def flush_type_buffer(self):
        """Gửi chuỗi ký tự đã gom được sang Android dưới dạng CLIP."""
        if not self.type_buffer:
            return
        text = "".join(self.type_buffer)
        self.type_buffer.clear()
        # Base64 encode để tránh lỗi ký tự đặc biệt qua UDP/text protocol đơn giản
        import base64
        encoded = base64.b64encode(text.encode('utf-8')).decode('ascii')
        self.send(f"CLIP {encoded}")
        print(f"[KEYBOARD] Đã gửi text sang clipboard điện thoại: '{text}'")

    def handle_key_event(self, key, pressed):
        """Xử lý sự kiện phím khi đang ở chế độ remote."""
        if not self.remote:
            return False # Cho phép pynput tiếp tục xử lý bình thường trên laptop
        
        now = time.time()
        
        # Timeout buffer nếu không gõ gì trong 0.5s -> auto flush
        if self.type_buffer and now - self.last_type_time > 0.5:
            self.flush_type_buffer()
            
        self.last_type_time = now

        try:
            char = key.char
        except AttributeError:
            char = None
            
        if char:
            # Là ký tự in được
            if pressed:
                self.type_buffer.append(char)
            return True # Consumed
            
        # Là phím đặc biệt
        k_name = str(key).replace("Key.", "").strip("'")
        
        if pressed:
            if k_name == 'enter':
                self.flush_type_buffer()
                self.send("KEY ENTER")
            elif k_name == 'backspace':
                self.flush_type_buffer()
                self.send("KEY BACKSPACE")
            elif k_name == 'esc':
                self.send("NAV BACK")
            elif k_name == 'home':
                self.send("NAV HOME")
            elif k_name == 'tab':
                self.send("KEY TAB")
            elif k_name in ('shift_l', 'shift_r'):
                self.modifiers['shift'] = True
            elif k_name in ('ctrl_l', 'ctrl_r'):
                self.modifiers['ctrl'] = True
            elif k_name in ('alt_l', 'alt_r'):
                self.modifiers['alt'] = True
                
        else: # Released
            if k_name in ('shift_l', 'shift_r'):
                self.modifiers['shift'] = False
            elif k_name in ('ctrl_l', 'ctrl_r'):
                self.modifiers['ctrl'] = False
            elif k_name in ('alt_l', 'alt_r'):
                self.modifiers['alt'] = False
                
        return True # Consumed

    def click(self, name):
        self.on_button(name, 1)
        self.on_button(name, 0)

    def pad_abs(self, d, ev):
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
                    d.scroll += -norm * 6.0   # cuộn tự nhiên
            else:
                delta = norm * 1800 * self.args.speed
                if axis == 0:
                    d.dx += delta
                else:
                    d.dy += delta
        d.last[axis] = ev.value

    def pad_key(self, d, ev):
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

    def flush_motion(self, d):
        if d.scroll:
            self.on_scroll(d.scroll)
            d.scroll = 0.0
        dx, dy = d.dx, d.dy
        d.dx = d.dy = 0.0
        if not (dx or dy):
            return
        
        # Nếu đang kéo (left button down), tính thêm quãng đường di chuyển thực tế
        if self.remote and hasattr(self, 'drag_start_time') and getattr(self, 'held_buttons', {}).get('L', False):
            import math
            dist = math.hypot(dx, dy)
            self.drag_total_dist += dist
            
        if self.remote:
            self.pend_dx += dx
            self.pend_dy += dy
        else:
            self.check_edge(dx, dy)

    def on_input(self, d, ev):
        if ev.type == e.EV_REL and not d.is_pad:
            if ev.code == e.REL_X:
                d.dx += ev.value * self.args.speed
            elif ev.code == e.REL_Y:
                d.dy += ev.value * self.args.speed
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

    def on_keyboard(self, ev):
        if ev.type != e.EV_KEY:
            return
        if ev.value:
            self.held.add(ev.code)
        else:
            self.held.discard(ev.code)
        ctrl = e.KEY_LEFTCTRL in self.held or e.KEY_RIGHTCTRL in self.held
        alt = e.KEY_LEFTALT in self.held or e.KEY_RIGHTALT in self.held
        if ev.code == e.KEY_M and ev.value == 1 and ctrl and alt:
            if self.remote:
                self.leave_remote(ratio=None, notify=True)
            else:
                self.enter_remote(0.5)

    # ---------- vòng lặp chính ----------
    def run(self):
        sources = {self.sock.fileno(): ("sock", None)}
        for d in self.mice:
            sources[d.dev.fd] = ("mouse", d)
        for k in self.keyboards:
            sources[k.fd] = ("kbd", k)
        self.send("PING")
        try:
            while True:
                pending = bool(self.pend_dx or self.pend_dy)
                ready, _, _ = select.select(list(sources), [], [], 0.01 if pending else 0.5)
                for fd in ready:
                    kind, obj = sources[fd]
                    try:
                        if kind == "sock":
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
                        print("Thiết bị bị rút ra, bỏ qua.")
                        sources.pop(fd, None)
                if self.remote:
                    self.flush_pending()
        finally:
            self.leave_remote(ratio=None, notify=True)


def main():
    p = argparse.ArgumentParser(description="AirMouse - gửi chuột laptop sang Android")
    p.add_argument("--phone", required=True, help="địa chỉ IP của điện thoại (xem trong app AirMouse)")
    p.add_argument("--secret", default="1234", help="mật khẩu, phải trùng với app (mặc định 1234)")
    p.add_argument("--port", type=int, default=5005, help="cổng UDP của điện thoại")
    p.add_argument("--listen-port", type=int, default=5006, help="cổng UDP laptop lắng nghe")
    p.add_argument("--speed", type=float, default=1.6, help="tốc độ con trỏ trên điện thoại")
    p.add_argument("--edge-push", type=float, default=40, help="độ 'đẩy' qua mép để chuyển (tăng nếu hay bị chuyển nhầm)")
    p.add_argument("--no-edge", action="store_true", help="tắt chuyển bằng mép, chỉ dùng Ctrl+Alt+M")
    p.add_argument("--blind-edge", action="store_true", help="Wayland: chuyển bằng mép theo ước lượng (kém chính xác)")
    
    p.add_argument("--screen-width", type=int, help="độ rộng màn hình (px) nếu tự nhận sai")
    p.add_argument("--screen-height", type=int, help="chiều cao màn hình (px) nếu tự nhận sai")
    args = p.parse_args()

    mice, keyboards = find_devices()
    if not mice:
        sys.exit(
            "Không tìm thấy chuột/touchpad nào (hoặc không có quyền đọc /dev/input).\n"
            "Chạy: sudo usermod -aG input $USER  rồi đăng xuất/đăng nhập lại, hoặc chạy bằng sudo."
        )
    print("Thiết bị chuột:", ", ".join(d.dev.name for d in mice))
    if not keyboards:
        print("⚠ Không đọc được bàn phím -> phím tắt Ctrl+Alt+M sẽ không dùng được.")

    size = get_screen_size()
    sw = args.screen_width or (size[0] if size else 1920)
    sh = args.screen_height or (size[1] if size else 1080)
    if not size and not (args.screen_width and args.screen_height):
        print("⚠ Không đọc được kích thước màn hình, dùng 1920x1080. Có thể chỉnh bằng --screen-width/--screen-height")

    ctl = None
    wayland = os.environ.get("XDG_SESSION_TYPE", "").lower() == "wayland"
    if not wayland and not args.no_edge:
        try:
            from pynput.mouse import Controller
            ctl = Controller()
            _ = ctl.position
        except Exception as ex:
            print("⚠ Không dùng được pynput (", ex, ") -> không phát hiện được mép màn hình.")
            ctl = None
    if args.no_edge:
        print("Chuyển bằng mép: TẮT. Dùng Ctrl+Alt+M.")
    elif ctl:
        print(f"Chuyển bằng mép: BẬT (màn hình {sw}x{sh}). Đẩy chuột sang phải để sang điện thoại.")
    elif args.blind_edge:
        print("Wayland: chuyển bằng mép theo ước lượng (blind). Có thể chuyển nhầm, hãy tăng --edge-push nếu cần.")
    else:
        print("Wayland: không đọc được vị trí con trỏ -> chỉ dùng Ctrl+Alt+M (hoặc thêm --blind-edge).")

    bridge = Bridge(args, mice, keyboards, ctl, sw, sh)
    
    # Gắn Keyboard Listener từ pynput nếu có
    kbd_listener_obj = None
    if kb_listener:
        try:
            def on_press(key):
                return bridge.handle_key_event(key, True)
            def on_release(key):
                return bridge.handle_key_event(key, False)
            
            kbd_listener_obj = kb_listener.Listener(on_press=on_press, on_release=on_release)
            kbd_listener_obj.start()
            print("✔ Đã bật chế độ điều khiển bàn phím từ xa (gõ text sẽ được gửi sang Clipboard Android).")
        except Exception as ex:
            print(f"Cảnh báo: Không khởi tạo được keyboard listener: {ex}")
            print("-> Tính năng gõ phím từ xa sẽ KHÔNG hoạt động.")
    else:
        print("⚠ Thiếu thư viện 'pynput'. Cài đặt: sudo apt install python3-pynput")
        print("-> Tính năng gõ phím từ xa sẽ KHÔNG hoạt động.")

    try:
        bridge.run()
    finally:
        if kbd_listener_obj:
            kbd_listener_obj.stop()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nĐã thoát.")
