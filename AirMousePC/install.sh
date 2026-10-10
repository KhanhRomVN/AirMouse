#!/usr/bin/env bash
set -e
sudo apt update
sudo apt install -y python3-evdev python3-pynput python3-tk
sudo usermod -aG input "$USER"
echo
echo "Xong. Hãy ĐĂNG XUẤT rồi ĐĂNG NHẬP lại (để quyền nhóm 'input' có hiệu lực)."
echo "Sau đó chạy:  python3 airmouse_laptop.py --phone <IP điện thoại>"
