"""Cấu hình dùng chung cho CLI và GUI (lưu tại ~/.config/airmouse/config.json)."""
from __future__ import annotations

import json
import os
import socket
from dataclasses import asdict, dataclass, fields
from pathlib import Path
from typing import Optional

CONFIG_DIR = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "airmouse"
CONFIG_FILE = CONFIG_DIR / "config.json"

# Các trường được lưu lại giữa các lần chạy
PERSISTED = ("phone", "secret", "speed", "edge_enabled", "blind_edge", "edge_push")


@dataclass
class Settings:
    phone: str = ""                 # IP điện thoại
    secret: str = "1234"            # mật khẩu (phải trùng với app)
    port: int = 5005                # cổng UDP của điện thoại
    listen_port: int = 5006         # cổng UDP laptop lắng nghe
    speed: float = 1.6              # tốc độ con trỏ trên điện thoại
    edge_push: float = 40.0         # độ "đẩy" qua mép để chuyển
    edge_enabled: bool = True       # chuyển bằng mép màn hình
    blind_edge: bool = False        # Wayland: chuyển bằng mép theo ước lượng
    screen_width: Optional[int] = None
    screen_height: Optional[int] = None

    # ---- lưu / nạp ----
    @classmethod
    def load(cls) -> "Settings":
        s = cls()
        try:
            data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return s
        known = {f.name: f for f in fields(cls)}
        for key in PERSISTED:
            if key in data and key in known:
                try:
                    setattr(s, key, type(getattr(s, key))(data[key]))
                except (TypeError, ValueError):
                    pass
        return s

    def save(self) -> None:
        try:
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            data = {k: v for k, v in asdict(self).items() if k in PERSISTED}
            CONFIG_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        except OSError:
            pass


def local_ip() -> str:
    """IP LAN của laptop (không gửi gói tin nào ra ngoài)."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("10.255.255.255", 1))
            return s.getsockname()[0]
    except OSError:
        return "—"


def valid_ipv4(text: str) -> bool:
    parts = text.strip().split(".")
    if len(parts) != 4:
        return False
    try:
        return all(p.isdigit() and 0 <= int(p) <= 255 for p in parts)
    except ValueError:
        return False
