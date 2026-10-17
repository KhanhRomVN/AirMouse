# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
# AirMouse

Biến chuột/touchpad của laptop Ubuntu thành chuột (và bàn phím gõ nhanh) không dây cho điện thoại Android qua Wi-Fi.
Cả hai phía đều có giao diện hiện đại, tối giản.

## Cấu trúc dự án

```
AirMouse/
├── airmouse_laptop.py     # điểm chạy chính (GUI mặc định, CLI khi có --phone)
├── airmouse/              # source chính — phần PC
│   ├── core.py            #   lõi: đọc evdev, chuyển mép, giao thức UDP
│   ├── gui.py             #   giao diện tkinter (tối, bo góc, hoạt ảnh trạng thái)
│   ├── cli.py             #   chế độ dòng lệnh
│   └── config.py          #   cấu hình, lưu ở ~/.config/airmouse/config.json
├── requirements.txt
├── install.sh
└── android/               # app Android (Kotlin, không phụ thuộc thư viện ngoài)
```

## Tính năng
- **Chuột cảm ứng**: di chuyển, click, kéo thả, cuộn dọc/ngang (Ctrl + cuộn).
- **Bàn phím từ xa**: gõ trên laptop → tự copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc = Back, Home = Home.
- **Chuyển mượt**: đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về; hoặc `Alt+M` chuyển qua lại thủ công.
- **Giao diện**: trạng thái kết nối trực tiếp (ping định kỳ, tự phát hiện mất kết nối), chỉnh tốc độ/độ nhạy mép ngay lúc chạy.

## Yêu cầu
- Laptop: Ubuntu 20.04+, Python 3.8+.
- Điện thoại: Android 8.0 (API 26) trở lên.
- Cùng một mạng Wi-Fi.

## Cài đặt

### Laptop
```bash
./install.sh            # cài evdev, pynput, tkinter + thêm quyền nhóm 'input'
# đăng xuất rồi đăng nhập lại
python3 airmouse_laptop.py
```
Hoặc dùng venv: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
(tkinter cần cài riêng: `sudo apt install python3-tk`).

### Android
Xem [android/README.md](android/README.md). Tóm tắt:
```bash
cd android
./gradlew assembleRelease     # APK: app/build/outputs/apk/release/AirMouse.apk
```
Cài APK, mở app, bấm **Bật trong Cài đặt Trợ năng** → AirMouse → bật.

## Sử dụng
1. Mở app AirMouse trên điện thoại, xem **địa chỉ điện thoại** (chạm để sao chép).
2. Trên laptop mở giao diện: `python3 airmouse_laptop.py`, nhập IP + mật khẩu (mặc định `1234`, phải trùng với app) → **Kết nối**.
   Hoặc dòng lệnh: `python3 airmouse_laptop.py --phone 192.168.x.x [--secret MATKHAU] [--blind-edge]`
3. Điều khiển:
   - Đẩy chuột sang mép phải laptop → con trỏ xuất hiện trên điện thoại. Kéo ra mép trái (hoặc `Ctrl+Alt+M`) để quay về.
   - Chuột trái = chạm / giữ / kéo · lăn = cuộn dọc · `Ctrl`+lăn = cuộn ngang · chuột phải = Back · chuột giữa = Home.
   - Touchpad: chạm nhanh = click, 2 ngón chạm = Back, 2 ngón trượt = cuộn.
   - Gõ chữ khi đang điều khiển → sau 0.5s ngừng gõ, text vào Clipboard điện thoại; giữ vào ô nhập → Dán.

### Tham số dòng lệnh
| Tham số | Ý nghĩa |
|---|---|
| `--phone IP` | IP điện thoại; có tham số này sẽ chạy CLI (không có = mở GUI) |
| `--gui` | Ép mở giao diện |
| `--secret MATKHAU` | Mật khẩu, trùng với app (mặc định `1234`) |
| `--speed 1.6` | Tốc độ con trỏ |
| `--edge-push 40` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Alt+M |
| `--blind-edge` | Wayland: chuyển bằng mép theo ước lượng |
| `--screen-width/--screen-height` | Khi nhiều màn hình hoặc nhận sai kích thước |

## Khắc phục sự cố
- **Không tìm thấy chuột**: `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc chạy bằng `sudo`).
- **Không mở được giao diện**: `sudo apt install python3-tk`; hoặc dùng CLI với `--phone`.
- **Wayland không chuyển được bằng mép**: bật “Mép ước lượng” (GUI) / `--blind-edge`, hoặc đăng nhập phiên Xorg, hoặc dùng `Ctrl+Alt+M`.
- **Không kết nối được**: kiểm tra cùng Wi-Fi, đúng IP & mật khẩu; Wi-Fi công cộng hay chặn thiết bị nói chuyện với nhau (thử hotspot); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không mã hoá — chỉ dùng trên mạng tin cậy.
