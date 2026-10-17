"""Chạy AirMouse bằng dòng lệnh (không cần giao diện)."""
from __future__ import annotations

import argparse
import sys
import time

from . import __version__
from .config import Settings
from .core import Engine

_ICON = {"info": "·", "ok": "✔", "warn": "⚠", "error": "✖"}


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="airmouse_laptop.py",
        description="AirMouse - dùng chuột laptop điều khiển Android. Không có tham số = mở giao diện.",
    )
    p.add_argument("--phone", help="IP điện thoại (xem trong app AirMouse). Có tham số này sẽ chạy chế độ dòng lệnh")
    p.add_argument("--secret", help="mật khẩu, phải trùng với app (mặc định 1234)")
    p.add_argument("--port", type=int, default=5005, help="cổng UDP của điện thoại")
    p.add_argument("--listen-port", type=int, default=5006, help="cổng UDP laptop lắng nghe")
    p.add_argument("--speed", type=float, help="tốc độ con trỏ trên điện thoại (mặc định 1.6)")
    p.add_argument("--edge-push", type=float, help="độ 'đẩy' qua mép để chuyển (mặc định 40)")
    p.add_argument("--no-edge", action="store_true", help="tắt chuyển bằng mép, chỉ dùng Alt+M")
    p.add_argument("--blind-edge", action="store_true", help="Wayland: chuyển bằng mép theo ước lượng")
    p.add_argument("--screen-width", type=int, help="độ rộng màn hình (px) nếu tự nhận sai")
    p.add_argument("--screen-height", type=int, help="chiều cao màn hình (px) nếu tự nhận sai")
    p.add_argument("--gui", action="store_true", help="ép mở giao diện đồ hoạ")
    p.add_argument("--version", action="version", version=f"AirMouse {__version__}")
    return p


def settings_from_args(args: argparse.Namespace) -> Settings:
    s = Settings.load()
    if args.phone:
        s.phone = args.phone
    if args.secret is not None:
        s.secret = args.secret
    if args.speed is not None:
        s.speed = args.speed
    if args.edge_push is not None:
        s.edge_push = args.edge_push
    if args.no_edge:
        s.edge_enabled = False
    if args.blind_edge:
        s.blind_edge = True
    s.port = args.port
    s.listen_port = args.listen_port
    s.screen_width = args.screen_width
    s.screen_height = args.screen_height
    return s


def run_cli(args: argparse.Namespace) -> int:
    cfg = settings_from_args(args)

    def emit(kind: str, **data) -> None:
        if kind == "log":
            print(f"{_ICON.get(data['level'], '·')} {data['text']}", flush=True)

    engine = Engine(cfg, emit)
    if not engine.start():
        return 1
    try:
        while engine.running:
            time.sleep(0.3)
    except KeyboardInterrupt:
        print("\nĐã thoát.")
    finally:
        engine.stop()
    return 0


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    if args.gui or not args.phone:
        try:
            from .gui import run_gui
        except ImportError as ex:
            if args.gui:
                print(f"Không mở được giao diện: {ex}\nCài đặt: sudo apt install python3-tk", file=sys.stderr)
                return 1
            print("Thiếu tkinter nên không mở được giao diện (sudo apt install python3-tk).", file=sys.stderr)
            print("Hoặc chạy dòng lệnh:  python3 airmouse_laptop.py --phone <IP điện thoại>", file=sys.stderr)
            return 1
        return run_gui(settings_from_args(args))
    return run_cli(args)


if __name__ == "__main__":
    raise SystemExit(main())
