# AirMouse – phần Laptop (Ubuntu)

Dùng chuột/touchpad của laptop để điều khiển điện thoại Android qua Wi-Fi.
Cần cài kèm app **AirMouse** (project Android trong file zip còn lại) trên điện thoại.

## 1. Cài đặt (1 lần)
```bash
./install.sh
```
Rồi **đăng xuất và đăng nhập lại** (để có quyền đọc chuột trong /dev/input).

## 2. Chạy
1. Điện thoại và laptop cùng một mạng Wi-Fi.
2. Mở app AirMouse trên điện thoại, xem dòng "IP điện thoại".
3. Trên laptop:
```bash
python3 airmouse_laptop.py --phone 192.168.x.x
```
Thấy dòng `✔ Đã kết nối với điện thoại.` là thông.

## 3. Sử dụng
- Điện thoại đặt **bên phải** laptop. Đẩy chuột sang mép phải màn hình laptop → con trỏ xuất hiện trên điện thoại.
- Kéo con trỏ trên điện thoại ra mép trái → chuột quay về laptop.
- **Ctrl+Alt+M**: chuyển qua lại thủ công (luôn dùng được, cũng là cách thoát khi bị kẹt).
- Chuột: click trái = chạm, giữ chuột = nhấn giữ, kéo chuột khi giữ = vuốt/kéo, lăn chuột = cuộn,
  **chuột phải = Back**, **chuột giữa = Home**.
- Touchpad: chạm nhanh = click, chạm 2 ngón = chuột phải (Back), 2 ngón trượt = cuộn.

## Tuỳ chọn
| Tham số | Ý nghĩa |
|---|---|
| `--secret MATKHAU` | Mật khẩu, phải trùng trong app (mặc định `1234` – nên đổi) |
| `--speed 2.0` | Tăng/giảm tốc độ con trỏ trên điện thoại |
| `--edge-push 80` | Tăng nếu hay bị chuyển nhầm sang điện thoại |
| `--no-edge` | Tắt chuyển bằng mép, chỉ dùng Ctrl+Alt+M |
| `--blind-edge` | Dành cho Wayland (xem dưới) |
| `--screen-width/--screen-height` | Nếu nhiều màn hình hoặc nhận sai kích thước |

## Lưu ý Wayland / X11
Ubuntu mới mặc định dùng **Wayland**, nơi chương trình không đọc được vị trí con trỏ.
- Mặc định trên Wayland: chỉ dùng **Ctrl+Alt+M** để chuyển.
- Thêm `--blind-edge` để chuyển bằng mép theo ước lượng (kém chính xác hơn).
- Muốn chuyển bằng mép chính xác: đăng nhập bằng phiên **Ubuntu on Xorg** (chọn ở màn hình đăng nhập, biểu tượng bánh răng).

## Khắc phục sự cố
- *Không tìm thấy chuột*: chưa có quyền. Chạy `sudo usermod -aG input $USER` rồi đăng nhập lại (hoặc thử `sudo python3 ...`).
- *Không thấy "Đã kết nối"*: kiểm tra cùng Wi-Fi, đúng IP, đúng mật khẩu; một số Wi-Fi công cộng chặn thiết bị nói chuyện với nhau (bật hotspot từ điện thoại hoặc laptop để thử); firewall: `sudo ufw allow 5006/udp`.
- Mật khẩu chỉ là lớp bảo vệ đơn giản, gói tin không được mã hoá. Chỉ dùng trên mạng tin cậy.
