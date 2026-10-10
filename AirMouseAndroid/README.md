# AirMouse – phần Android

App nhận chuột từ laptop (qua Wi-Fi/UDP), vẽ con trỏ chuột lên màn hình và thực hiện thao tác chạm, giữ, kéo, cuộn, Back, Home.
Dùng dịch vụ **Trợ năng (AccessibilityService)** nên không cần root, không cần cáp.

## Build APK
1. Cài **Android Studio** (bản mới), chọn *Open* và trỏ tới thư mục này. Chờ Gradle sync
   (nếu Studio đề nghị nâng cấp phiên bản Gradle/AGP thì chấp nhận).
2. Bật Gỡ lỗi USB trên điện thoại, cắm cáp, bấm **Run ▶** để cài thẳng vào máy.
   Hoặc: *Build → Build APK(s)* rồi copy file `app/build/outputs/apk/debug/app-debug.apk` sang điện thoại để cài.

Dòng lệnh (nếu đã có Android SDK + Gradle): `gradle assembleDebug`

## Thiết lập trên điện thoại
1. Mở app AirMouse → **Mở cài đặt Trợ năng** → AirMouse → bật.
   Nếu nút bị mờ (Android 13+ với app cài ngoài Store): Cài đặt → Ứng dụng → AirMouse → ⋮ → *Cho phép cài đặt bị hạn chế*, rồi bật lại.
2. Đặt mật khẩu (trùng với `--secret` trên laptop; mặc định `1234`, nên đổi).
3. Ghi lại địa chỉ IP hiển thị trong app và dùng cho `--phone` trên laptop.

## Hạn chế đã biết
- Kéo-thả được thực hiện **sau khi nhả chuột** (phát lại đường kéo), nên chưa mượt theo thời gian thực.
- Màn hình nhập mật khẩu, một số app ngân hàng chặn dịch vụ Trợ năng nên không thao tác được.
- Chưa có chuột phải thật (chuột phải = Back), chưa có bàn phím.
- Gói tin UDP không mã hoá; chỉ dùng trên mạng tin cậy.
