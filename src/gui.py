"""Giao diện đồ hoạ (tkinter) cho AirMouse — tối, phẳng, bo góc, có hoạt ảnh trạng thái."""
from __future__ import annotations

import math
import os
import queue
import threading
import time
import tkinter as tk
from tkinter import font as tkfont

from . import __version__
from .config import Settings, local_ip, valid_ipv4
from .core import CONNECTED, CONNECTING, REMOTE, STOPPED, Engine

# ───────────────────────── Bảng màu (dùng chung tinh thần với app Android) ─────────────────────────
BG = "#0B0F1A"
SURFACE = "#131A2A"
SURFACE2 = "#1A2236"
SURFACE3 = "#222C45"
BORDER = "#242E49"
TEXT = "#E8ECF8"
MUTED = "#8A94B0"
FAINT = "#566080"
ACCENT = "#6C7BFF"
ACCENT_HI = "#8592FF"
ACCENT_LO = "#5867EA"
CYAN = "#22D3EE"
OK = "#34D399"
WARN = "#FBBF24"
ERR = "#F87171"


def blend(c1: str, c2: str, t: float) -> str:
    """Trộn màu c1→c2 theo t∈[0,1] (dùng để giả lập độ trong suốt)."""
    a = [int(c1[i : i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i : i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(a, b))


def rrect(c: tk.Canvas, x1, y1, x2, y2, r, **kw):
    r = max(0, min(r, (x2 - x1) / 2, (y2 - y1) / 2))
    pts = [
        x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r, x2, y2 - r, x2, y2,
        x2 - r, y2, x1 + r, y2, x1, y2, x1, y2 - r, x1, y1 + r, x1, y1,
    ]
    return c.create_polygon(pts, smooth=True, **kw)


def pick_font(root, candidates, default):
    have = set(tkfont.families(root))
    for f in candidates:
        if f in have:
            return f
    return default


# ───────────────────────── Widget tự vẽ ─────────────────────────
class Card(tk.Canvas):
    """Khung bo góc. Đặt nội dung vào `.inner`; chiều cao tự co theo nội dung."""

    def __init__(self, parent, parent_bg=BG, fill=SURFACE, border=BORDER, radius=16, padx=18, pady=16):
        super().__init__(parent, bg=parent_bg, highlightthickness=0, bd=0, height=10)
        self.fill, self.border, self.radius = fill, border, radius
        self.padx, self.pady = padx, pady
        self.inner = tk.Frame(self, bg=fill)
        self._win = self.create_window(padx, pady, anchor="nw", window=self.inner)
        self.bind("<Configure>", self._layout)
        self.inner.bind("<Configure>", self._layout)

    def set_border(self, color: str) -> None:
        self.border = color
        self._layout()

    def _layout(self, _evt=None):
        w = self.winfo_width()
        if w <= 1:
            return
        ih = self.inner.winfo_reqheight()
        h = ih + 2 * self.pady
        self.itemconfigure(self._win, width=max(1, w - 2 * self.padx))
        if int(float(self.cget("height"))) != h:
            self.configure(height=h)
        self.delete("bg")
        rrect(self, 1, 1, w - 1, h - 1, self.radius, fill=self.fill, outline=self.border, width=1, tags="bg")
        self.tag_lower("bg")


class Button(tk.Canvas):
    STYLES = {
        "primary": dict(fill=ACCENT, hover=ACCENT_HI, press=ACCENT_LO, fg="#FFFFFF", border=ACCENT),
        "secondary": dict(fill=SURFACE2, hover=SURFACE3, press=SURFACE, fg=TEXT, border=BORDER),
        "danger": dict(fill="#2A1822", hover="#36202B", press="#220F18", fg=ERR, border="#5A2A38"),
        "disabled": dict(fill=SURFACE, hover=SURFACE, press=SURFACE, fg=FAINT, border=BORDER),
    }

    def __init__(self, parent, text, command, font, style="primary", parent_bg=BG, height=46):
        super().__init__(parent, bg=parent_bg, highlightthickness=0, bd=0, height=height)
        self._text, self._cmd, self._font = text, command, font
        self._style, self._enabled = style, True
        self._hover = self._down = False
        self.bind("<Configure>", lambda _e: self._draw())
        self.bind("<Enter>", lambda _e: self._set(hover=True))
        self.bind("<Leave>", lambda _e: self._set(hover=False, down=False))
        self.bind("<ButtonPress-1>", lambda _e: self._set(down=True))
        self.bind("<ButtonRelease-1>", self._release)
        self.configure(cursor="hand2")

    def _set(self, hover=None, down=None):
        if hover is not None:
            self._hover = hover
        if down is not None:
            self._down = down
        self._draw()

    def _release(self, _e):
        was = self._down
        self._set(down=False)
        if was and self._hover and self._enabled and self._cmd:
            self._cmd()

    def configure_button(self, text=None, style=None, enabled=None):
        if text is not None:
            self._text = text
        if style is not None:
            self._style = style
        if enabled is not None:
            self._enabled = enabled
            self.configure(cursor="hand2" if enabled else "arrow")
        self._draw()

    def _draw(self):
        w, h = self.winfo_width(), self.winfo_height()
        if w <= 1:
            return
        s = self.STYLES["disabled" if not self._enabled else self._style]
        fill = s["press"] if (self._down and self._enabled) else s["hover"] if (self._hover and self._enabled) else s["fill"]
        self.delete("all")
        rrect(self, 1, 1, w - 1, h - 1, 12, fill=fill, outline=s["border"], width=1)
        self.create_text(w / 2, h / 2, text=self._text, fill=s["fg"], font=self._font)


class Toggle(tk.Canvas):
    W, H = 44, 24

    def __init__(self, parent, value, command, parent_bg=SURFACE):
        super().__init__(parent, width=self.W, height=self.H, bg=parent_bg, highlightthickness=0, bd=0, cursor="hand2")
        self.value, self._cmd, self._bg = bool(value), command, parent_bg
        self._pos = 1.0 if self.value else 0.0
        self.bind("<Button-1>", lambda _e: self.set(not self.value, notify=True))
        self._draw()

    def set(self, value: bool, notify=False):
        if value == self.value:
            return
        self.value = value
        if notify and self._cmd:
            self._cmd(value)
        self._animate()

    def _animate(self):
        target = 1.0 if self.value else 0.0
        self._pos += (target - self._pos) * 0.45
        if abs(target - self._pos) < 0.03:
            self._pos = target
        self._draw()
        if self._pos != target:
            self.after(16, self._animate)

    def _draw(self):
        self.delete("all")
        track = blend(SURFACE3, ACCENT, self._pos)
        rrect(self, 1, 1, self.W - 1, self.H - 1, self.H / 2, fill=track, outline=track)
        r = self.H / 2 - 4
        cx = 4 + r + self._pos * (self.W - 8 - 2 * r)
        self.create_oval(cx - r, self.H / 2 - r, cx + r, self.H / 2 + r, fill="#FFFFFF", outline="")


class Slider(tk.Canvas):
    def __init__(self, parent, lo, hi, value, step, command, parent_bg=SURFACE):
        super().__init__(parent, height=26, bg=parent_bg, highlightthickness=0, bd=0, cursor="hand2")
        self.lo, self.hi, self.step, self.value, self._cmd = lo, hi, step, value, command
        self.bind("<Configure>", lambda _e: self._draw())
        self.bind("<Button-1>", self._drag)
        self.bind("<B1-Motion>", self._drag)

    def _drag(self, ev):
        w = self.winfo_width()
        pad = 10
        t = min(max((ev.x - pad) / max(1, w - 2 * pad), 0.0), 1.0)
        v = self.lo + t * (self.hi - self.lo)
        v = round(v / self.step) * self.step
        v = min(max(v, self.lo), self.hi)
        if v != self.value:
            self.value = v
            self._draw()
            if self._cmd:
                self._cmd(v)

    def _draw(self):
        w, h = self.winfo_width(), self.winfo_height()
        if w <= 1:
            return
        pad, cy = 10, h / 2
        t = (self.value - self.lo) / (self.hi - self.lo)
        x = pad + t * (w - 2 * pad)
        self.delete("all")
        rrect(self, pad, cy - 3, w - pad, cy + 3, 3, fill=SURFACE3, outline="")
        if x > pad:
            rrect(self, pad, cy - 3, x, cy + 3, 3, fill=ACCENT, outline="")
        self.create_oval(x - 11, cy - 11, x + 11, cy + 11, fill=blend(ACCENT, SURFACE, 0.78), outline="")
        self.create_oval(x - 8, cy - 8, x + 8, cy + 8, fill="#FFFFFF", outline="")


class StatusDot(tk.Canvas):
    """Chấm trạng thái, có vòng lan toả khi `pulse=True`."""

    SIZE = 48

    def __init__(self, parent, parent_bg=SURFACE):
        super().__init__(parent, width=self.SIZE, height=self.SIZE, bg=parent_bg, highlightthickness=0, bd=0)
        self._bg, self.color, self.pulse, self._t = parent_bg, MUTED, False, 0.0
        self.draw()

    def set(self, color: str, pulse: bool) -> None:
        self.color, self.pulse = color, pulse
        self.draw()

    def tick(self, dt: float) -> None:
        if self.pulse:
            self._t = (self._t + dt / 1.6) % 1.0
            self.draw()

    def draw(self) -> None:
        self.delete("all")
        c = self.SIZE / 2
        self.create_oval(c - 18, c - 18, c + 18, c + 18, fill=blend(self.color, self._bg, 0.86), outline="")
        if self.pulse:
            r = 9 + self._t * 15
            self.create_oval(c - r, c - r, c + r, c + r, outline=blend(self.color, self._bg, 0.25 + 0.75 * self._t), width=2)
        self.create_oval(c - 8, c - 8, c + 8, c + 8, fill=self.color, outline="")


class Field(tk.Frame):
    """Ô nhập có nhãn, viền đổi màu khi focus."""

    def __init__(self, parent, label, var, fonts, parent_bg=SURFACE, secret=False, hint=""):
        super().__init__(parent, bg=parent_bg)
        head = tk.Frame(self, bg=parent_bg)
        head.pack(fill="x")
        tk.Label(head, text=label, bg=parent_bg, fg=MUTED, font=fonts["small"]).pack(side="left")
        if hint:
            tk.Label(head, text=hint, bg=parent_bg, fg=FAINT, font=fonts["small"]).pack(side="right")
        self.box = Card(self, parent_bg=parent_bg, fill=SURFACE2, border=BORDER, radius=10, padx=12, pady=9)
        self.box.pack(fill="x", pady=(6, 0))
        row = tk.Frame(self.box.inner, bg=SURFACE2)
        row.pack(fill="x")
        self.entry = tk.Entry(
            row, textvariable=var, bg=SURFACE2, fg=TEXT, insertbackground=ACCENT, relief="flat",
            highlightthickness=0, bd=0, font=fonts["mono"], show="•" if secret else "",
            selectbackground=ACCENT, selectforeground="#FFFFFF",
        )
        self.entry.pack(side="left", fill="x", expand=True)
        self._secret = secret
        if secret:
            self._eye = tk.Label(row, text="Hiện", bg=SURFACE2, fg=MUTED, font=fonts["small"], cursor="hand2")
            self._eye.pack(side="right")
            self._eye.bind("<Button-1>", self._toggle)
        self.entry.bind("<FocusIn>", lambda _e: self.box.set_border(ACCENT))
        self.entry.bind("<FocusOut>", lambda _e: self.box.set_border(BORDER))

    def _toggle(self, _e):
        showing = self.entry.cget("show") == ""
        self.entry.configure(show="•" if showing else "")
        self._eye.configure(text="Hiện" if showing else "Ẩn")

    def flash_error(self):
        self.box.set_border(ERR)
        self.after(1200, lambda: self.box.set_border(BORDER))


# ───────────────────────── Ứng dụng ─────────────────────────
STATE_VIEW = {
    STOPPED: (MUTED, False, "Chưa kết nối", "Nhập IP điện thoại rồi bấm Kết nối."),
    CONNECTING: (WARN, True, "Đang tìm điện thoại…", "Mở app AirMouse trên điện thoại và bật Trợ năng."),
    CONNECTED: (OK, False, "Đã kết nối", "Đẩy chuột sang mép phải màn hình để điều khiển điện thoại."),
    REMOTE: (ACCENT, True, "Đang điều khiển điện thoại", "Alt+M hoặc kéo con trỏ ra mép trái để quay về."),
}


class App:
    def __init__(self, cfg: Settings):
        self.cfg = cfg
        self.root = root = tk.Tk()
        root.title("AirMouse")
        root.configure(bg=BG)
        root.geometry("900x640")
        root.minsize(820, 600)

        sans = pick_font(root, ["Inter", "SF Pro Display", "Segoe UI", "Ubuntu", "Cantarell", "Noto Sans", "DejaVu Sans"], "TkDefaultFont")
        mono = pick_font(root, ["JetBrains Mono", "Fira Code", "Ubuntu Mono", "DejaVu Sans Mono", "Courier New"], "TkFixedFont")
        self.fonts = {
            "title": (sans, 20, "bold"),
            "h2": (sans, 14, "bold"),
            "body": (sans, 10),
            "bodyb": (sans, 10, "bold"),
            "small": (sans, 9),
            "btn": (sans, 11, "bold"),
            "mono": (mono, 11),
            "log": (mono, 9),
            "cap": (sans, 8, "bold"),
        }

        if not cfg.screen_width or not cfg.screen_height:
            cfg.screen_width, cfg.screen_height = root.winfo_screenwidth(), root.winfo_screenheight()

        self.events: "queue.Queue[tuple[str, dict]]" = queue.Queue()
        self.engine = Engine(cfg, lambda kind, **data: self.events.put((kind, data)))
        self.state = STOPPED
        self._stopping = False

        self.phone_var = tk.StringVar(value=cfg.phone)
        self.secret_var = tk.StringVar(value=cfg.secret)

        self._build()
        self.apply_state(STOPPED)

        root.protocol("WM_DELETE_WINDOW", self.on_close)
        self._last = time.time()
        root.after(40, self._tick)

    # ---------- dựng giao diện ----------
    def _build(self):
        f = self.fonts
        root = self.root
        root.grid_columnconfigure(0, weight=1, uniform="col")
        root.grid_columnconfigure(1, weight=1, uniform="col")
        root.grid_rowconfigure(0, weight=1)

        left = tk.Frame(root, bg=BG)
        right = tk.Frame(root, bg=BG)
        left.grid(row=0, column=0, sticky="nsew", padx=(28, 12), pady=(24, 8))
        right.grid(row=0, column=1, sticky="nsew", padx=(12, 28), pady=(24, 8))

        # --- tiêu đề ---
        head = tk.Frame(left, bg=BG)
        head.pack(fill="x")
        logo = tk.Canvas(head, width=46, height=46, bg=BG, highlightthickness=0)
        rrect(logo, 1, 1, 45, 45, 13, fill=ACCENT, outline="")
        logo.create_polygon(
            [15, 10, 15, 34, 21, 28, 26, 38, 30, 36, 25, 27, 33, 27], fill="#FFFFFF", outline=""
        )
        logo.pack(side="left")
        titles = tk.Frame(head, bg=BG)
        titles.pack(side="left", padx=(12, 0))
        tk.Label(titles, text="AirMouse", bg=BG, fg=TEXT, font=f["title"]).pack(anchor="w")
        tk.Label(titles, text="Chuột & bàn phím không dây cho Android", bg=BG, fg=MUTED, font=f["small"]).pack(anchor="w")

        # --- thẻ trạng thái ---
        self.status = Card(left, padx=18, pady=16)
        self.status.pack(fill="x", pady=(22, 14))
        row = tk.Frame(self.status.inner, bg=SURFACE)
        row.pack(fill="x")
        self.dot = StatusDot(row)
        self.dot.pack(side="left")
        txt = tk.Frame(row, bg=SURFACE)
        txt.pack(side="left", padx=(10, 0), fill="x", expand=True)
        self.status_title = tk.Label(txt, text="", bg=SURFACE, fg=TEXT, font=f["h2"], anchor="w")
        self.status_title.pack(fill="x")
        self.status_sub = tk.Label(txt, text="", bg=SURFACE, fg=MUTED, font=f["small"], anchor="w", justify="left", wraplength=290)
        self.status_sub.pack(fill="x", pady=(2, 0))

        # --- thẻ kết nối ---
        conn = Card(left)
        conn.pack(fill="x")
        tk.Label(conn.inner, text="KẾT NỐI", bg=SURFACE, fg=FAINT, font=f["cap"]).pack(anchor="w")
        self.phone_field = Field(conn.inner, "IP điện thoại", self.phone_var, f, hint="xem trong app")
        self.phone_field.pack(fill="x", pady=(10, 0))
        Field(conn.inner, "Mật khẩu", self.secret_var, f, secret=True, hint="phải trùng với app").pack(fill="x", pady=(12, 0))

        # --- nút ---
        self.btn_main = Button(left, "Kết nối", self.on_main, f["btn"], "primary")
        self.btn_main.pack(fill="x", pady=(14, 0))
        self.btn_remote = Button(left, "Chuyển chuột sang điện thoại", self.engine.toggle_remote, f["btn"], "secondary")
        self.btn_remote.pack(fill="x", pady=(10, 0))

        # --- thẻ tuỳ chọn ---
        opts = Card(right)
        opts.pack(fill="x")
        tk.Label(opts.inner, text="TUỲ CHỌN", bg=SURFACE, fg=FAINT, font=f["cap"]).pack(anchor="w")

        self.speed_lbl = self._slider_row(opts.inner, "Tốc độ con trỏ", 0.5, 4.0, self.cfg.speed, 0.1,
                                          self._on_speed, lambda v: f"{v:.1f}×")
        self.push_lbl = self._slider_row(opts.inner, "Độ nặng khi đẩy qua mép", 10, 150, self.cfg.edge_push, 5,
                                         self._on_push, lambda v: f"{int(v)}")
        self._switch_row(opts.inner, "Chuyển bằng mép màn hình", "Đẩy chuột sang mép phải để sang điện thoại",
                         self.cfg.edge_enabled, self._on_edge)
        wayland = os.environ.get("XDG_SESSION_TYPE", "").lower() == "wayland"
        self._switch_row(opts.inner, "Mép ước lượng (Wayland)",
                         "Phiên Wayland hiện tại — nên bật" if wayland else "Chỉ cần khi dùng Wayland",
                         self.cfg.blind_edge, self._on_blind)

        # --- nhật ký ---
        logcard = Card(right)
        logcard.pack(fill="both", expand=True, pady=(14, 0))
        top = tk.Frame(logcard.inner, bg=SURFACE)
        top.pack(fill="x")
        tk.Label(top, text="NHẬT KÝ", bg=SURFACE, fg=FAINT, font=f["cap"]).pack(side="left")
        clear = tk.Label(top, text="Xoá", bg=SURFACE, fg=MUTED, font=f["small"], cursor="hand2")
        clear.pack(side="right")
        clear.bind("<Button-1>", lambda _e: self._clear_log())
        self.log = tk.Text(
            logcard.inner, height=9, bg=SURFACE, fg=TEXT, font=f["log"], relief="flat", bd=0,
            highlightthickness=0, wrap="word", state="disabled", cursor="arrow", spacing1=2, spacing3=2,
            selectbackground=ACCENT,
        )
        self.log.pack(fill="both", expand=True, pady=(8, 0))
        for tag, col in (("info", MUTED), ("ok", OK), ("warn", WARN), ("error", ERR), ("time", FAINT)):
            self.log.tag_configure(tag, foreground=col)

        # --- chân trang ---
        foot = tk.Frame(root, bg=BG)
        foot.grid(row=1, column=0, columnspan=2, sticky="ew", padx=28, pady=(0, 14))
        self.chip(foot, f"Laptop  {local_ip()}").pack(side="left")
        self.chip(foot, "Alt + M  chuyển nhanh").pack(side="left", padx=(8, 0))
        tk.Label(foot, text=f"v{__version__}", bg=BG, fg=FAINT, font=f["small"]).pack(side="right")

    def chip(self, parent, text):
        return tk.Label(parent, text=text, bg=SURFACE, fg=MUTED, font=self.fonts["small"], padx=10, pady=4)

    def _slider_row(self, parent, label, lo, hi, value, step, cmd, fmt):
        f = self.fonts
        wrap = tk.Frame(parent, bg=SURFACE)
        wrap.pack(fill="x", pady=(14, 0))
        head = tk.Frame(wrap, bg=SURFACE)
        head.pack(fill="x")
        tk.Label(head, text=label, bg=SURFACE, fg=TEXT, font=f["body"]).pack(side="left")
        val = tk.Label(head, text=fmt(value), bg=SURFACE, fg=ACCENT_HI, font=f["bodyb"])
        val.pack(side="right")

        def on(v):
            val.configure(text=fmt(v))
            cmd(v)

        Slider(wrap, lo, hi, value, step, on).pack(fill="x", pady=(4, 0))
        return val

    def _switch_row(self, parent, title, desc, value, cmd):
        f = self.fonts
        row = tk.Frame(parent, bg=SURFACE)
        row.pack(fill="x", pady=(16, 0))
        col = tk.Frame(row, bg=SURFACE)
        col.pack(side="left", fill="x", expand=True)
        tk.Label(col, text=title, bg=SURFACE, fg=TEXT, font=f["body"], anchor="w").pack(fill="x")
        tk.Label(col, text=desc, bg=SURFACE, fg=MUTED, font=f["small"], anchor="w").pack(fill="x")
        Toggle(row, value, cmd).pack(side="right")

    # ---------- nhật ký ----------
    def add_log(self, level: str, text: str):
        self.log.configure(state="normal")
        self.log.insert("end", time.strftime("%H:%M:%S  "), "time")
        self.log.insert("end", text + "\n", level if level in ("info", "ok", "warn", "error") else "info")
        lines = int(self.log.index("end-1c").split(".")[0])
        if lines > 300:
            self.log.delete("1.0", f"{lines - 300}.0")
        self.log.see("end")
        self.log.configure(state="disabled")

    def _clear_log(self):
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.configure(state="disabled")

    # ---------- trạng thái ----------
    def apply_state(self, state: str):
        self.state = state
        color, pulse, title, sub = STATE_VIEW[state]
        self.dot.set(color, pulse)
        self.status_title.configure(text=title)
        if state == CONNECTING and self.cfg.phone:
            sub = f"Đang gửi tín hiệu tới {self.cfg.phone}…"
        self.status_sub.configure(text=sub)

        running = state != STOPPED
        if self._stopping:
            self.btn_main.configure_button(text="Đang dừng…", style="disabled", enabled=False)
        elif running:
            self.btn_main.configure_button(text="Ngắt kết nối", style="danger", enabled=True)
        else:
            self.btn_main.configure_button(text="Kết nối", style="primary", enabled=True)

        if state == REMOTE:
            self.btn_remote.configure_button(text="Trả chuột về laptop", style="primary", enabled=True)
        else:
            self.btn_remote.configure_button(
                text="Chuyển chuột sang điện thoại",
                style="secondary" if state == CONNECTED else "disabled",
                enabled=state == CONNECTED,
            )

    # ---------- hành động ----------
    def on_main(self):
        if self._stopping:
            return
        if self.engine.running:
            self._stopping = True
            self.apply_state(self.state)

            def work():
                self.engine.stop()
                self.events.put(("stopped_by_user", {}))

            threading.Thread(target=work, daemon=True).start()
            return

        phone = self.phone_var.get().strip()
        if not valid_ipv4(phone):
            self.phone_field.flash_error()
            self.add_log("error", "IP điện thoại chưa hợp lệ (ví dụ 192.168.1.50).")
            return
        self.cfg.phone = phone
        self.cfg.secret = self.secret_var.get().strip() or "1234"
        self.cfg.save()
        if self.engine.start():
            self.apply_state(CONNECTING)

    def _on_speed(self, v):
        self.cfg.speed = float(v)
        self.cfg.save()

    def _on_push(self, v):
        self.cfg.edge_push = float(v)
        self.cfg.save()

    def _on_edge(self, v):
        self.cfg.edge_enabled = bool(v)
        self.cfg.save()
        if self.engine.running:
            self.add_log("warn", "Kết nối lại để áp dụng thay đổi chuyển bằng mép.")

    def _on_blind(self, v):
        self.cfg.blind_edge = bool(v)
        self.cfg.save()

    # ---------- vòng lặp ----------
    def _tick(self):
        now = time.time()
        dt, self._last = now - self._last, now
        self.dot.tick(dt)
        try:
            while True:
                kind, data = self.events.get_nowait()
                if kind == "log":
                    self.add_log(data["level"], data["text"])
                elif kind == "state":
                    if not self._stopping or data["state"] == STOPPED:
                        self.apply_state(data["state"])
                elif kind == "stopped_by_user":
                    self._stopping = False
                    self.apply_state(STOPPED)
        except queue.Empty:
            pass
        self.root.after(40, self._tick)

    def on_close(self):
        self.cfg.phone = self.phone_var.get().strip()
        self.cfg.secret = self.secret_var.get().strip() or "1234"
        self.cfg.save()
        try:
            self.engine.stop()
        finally:
            self.root.destroy()

    def run(self):
        self.root.mainloop()


def run_gui(cfg: Settings) -> int:
    App(cfg).run()
    return 0
