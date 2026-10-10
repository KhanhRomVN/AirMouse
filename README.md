# AirMouse

Biến laptop Ubuntu thành bàn phím & chuột không dây cho điện thoại Android qua Wi-Fi.

## Tính năng chính
- **Chuột cảm ứng**: Di chuyển con trỏ, click, kéo thả, cuộn dọc/ngang (Ctrl+Scroll).
- **Bàn phím từ xa**: Gõ text trên laptop -> Tự động copy vào Clipboard điện thoại.
- **Phím điều hướng**: Esc (Back), Home (Home).
- **Chuyển đổi mượt mà**: Đẩy chuột sang mép phải màn hình laptop để sang điện thoại, kéo ra mép trái để quay về. Hoặc dùng tổ hợp `Ctrl+Alt+M`.

## Yêu cầu hệ thống
- **Laptop**: Ubuntu 20.04+, Python 3.8+.
- **Điện thoại**: Android 8.0 (API 26) trở lên.
- Cả hai thiết bị phải cùng một mạng Wi-Fi.

## Cài đặt

### 1. Phía Laptop (Python)
Tạo môi trường ảo và cài đặt dependencies:
```bash
cd AirMousePC
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
*Cấp quyền đọc thiết bị input (nếu cần):*
```bash
sudo usermod -aG input $USER
# Đăng xuất rồi đăng nhập lại
```

### 2. Phía Android
Tải file `AirMouse.apk` từ thư mục `AirMouseAndroid/app/build/outputs/apk/release/` (sau khi build) hoặc clone repo và build bằng Gradle:
```bash
cd AirMouseAndroid
./gradlew assembleRelease
# File APK nằm tại: app/build/outputs/apk/release/AirMouse.apk
```
Cài đặt APK lên điện thoại. Mở App và ghi nhớ địa chỉ IP hiển thị. Bật Quyền Trợ Năng (Accessibility Service) cho AirMouse.

## Cách sử dụng

1. Chạy script trên laptop:
   ```bash
   cd AirMousePC
   source .venv/bin/activate
   python3 airmouse_laptop.py --phone <IP_ĐIỆN_THOẠI> [--blind-edge]
   ```
   *(Thêm `--blind-edge` nếu bạn dùng Wayland/GNOME mặc định để hỗ trợ chuyển đổi bằng mép màn hình).*

2. Trên điện thoại, mở App AirMouse. Đảm bảo mật khẩu trùng khớp (mặc định là `1234`).

3. **Điều khiển**:
   - **Di chuột**: Push chuột sang mép phải màn hình laptop. Con trỏ sẽ xuất hiện trên điện thoại.
   - **Quay về laptop**: Kéo con trỏ trên điện thoại ra mép trái, hoặc nhấn `Ctrl+Alt+M`.
   - **Click/Kéo**: Chuột trái = Chạm/Kéo. Giữ chuột trái + di chuyển = Vuốt/Kéo thả.
   - **Cuộn**: Lăn chuột = Cuộn dọc. `Ctrl` + Lăn chuột = Cuộn ngang.
   - **Gõ phím**: Khi đang ở chế độ remote, gõ chữ trên laptop. Text sẽ tự động được sao chép vào Clipboard điện thoại sau 0.5s ngừng gõ. Bạn có thể Long-press vào ô nhập liệu trên Android để Dán.
   - **Phím tắt**: 
     - `Esc`: Nút Back.
     - `Home`: Nút Home.

## Khắc phục sự cố
- **"Thiếu thư viện evdev/pynput"**: Hãy chắc chắn bạn đã activate `.venv` (`source .venv/bin/activate`) trước khi chạy lệnh python.
- **Không chuyển được bằng mép (Wayland)**: Thêm tham số `--blind-edge`.
- **Không kết nối được**: Kiểm tra tường lửa (`sudo ufw allow 5005/udp`, `sudo ufw allow 5006/udp`), đảm bảo cùng subnet Wi-Fi.