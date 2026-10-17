#!/usr/bin/env python3
"""
AirMouse – điểm chạy chính của phần PC.

    python3 airmouse_laptop.py                       # mở giao diện
    python3 airmouse_laptop.py --phone 192.168.1.50  # chạy dòng lệnh
"""
from src.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
