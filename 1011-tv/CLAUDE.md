# 1011 TV: ghi chú cho Claude

Launcher Android TV cho một hộp FPT Play 650 (Android 14, 1080p, ADB qua mạng ở `192.168.1.2:5555`).
Mọi chỉnh sửa làm thẳng trong code; không có theme hay màn hình cài đặt.

## Cấu trúc launcher (`launcher/app/src/main/java/com/gathin/tvhome/`)

- `MainActivity`: lưới, viền focus (`FocusRing`), điều hướng D-pad, menu bánh răng (Mạng, Ẩn/hiện, Cài đặt),
  menu giữ OK trên ô, chế độ tick Ẩn/hiện ứng dụng.
- `AppAdapter`: dựng danh sách ô, kích thước ô (16:9, khoảng cách 18dp, vừa `rows` hàng), sắp theo
  `LaunchCounts` rồi theo tên.
- `LaunchCounts`: đếm số lần mở app từ UsageStats (cần `appops set com.gathin.tvhome GET_USAGE_STATS allow`).
- `LibraryApps`: lưu lựa chọn ẩn/hiện.
- `Config` đọc `res/values/config.xml`. Màu nền ở `res/values/colors.xml`.
- `ClockActivity`/`ClockDream`/`ClockScene`: đồng hồ bảo vệ màn hình.
- `LiveClockBanner`: ô của app Đồng Hồ (`io.github.playmakerino.clock`, ở `tre-em/android`) là đồng hồ số chạy thật
  (giờ:phút 24 giờ, màu theo trang `dong-ho.html`); font Space Grotesk ở `res/font/`.

## Làm việc với hộp

- Build và cài: `launcher\build-and-install.ps1 -TvHost 192.168.1.2` (PowerShell).
- Lệnh shell trên hộp: `TV_HOST=192.168.1.2 tools/venv/Scripts/python -I tools/tv.py '<lệnh>'`;
  chụp màn hình: `tools/tv.py --screenshot shots/x.png [PHÍM]`.
- Kiểm tra trước khi cài: `gradlew.bat lintRelease testReleaseUnitTest` trong `launcher/`.
- Không tắt gói lõi Android hay gói nhà máy (`com.hisense.bigfac`, `com.example.facservicetest`).
  Tắt app bằng `tools/disable.sh <danh sách>`, không gỡ app hệ thống.
- Cổng ADB 5555 được giữ mở theo ý chủ máy.
- `com.fptplay.launcher` vừa là launcher gốc vừa là app xem FPT Play (một gói, tự cập nhật, chạy quyền hệ thống
  `android.uid.system`, ~135-200 MB RAM khi chạy). Từ 25/10/2026 gói này bị tắt bằng
  `pm disable-user --user 0 com.fptplay.launcher`; chủ máy xem FPT Play bằng bản Play Store `net.fptplay.ottbox`
  (cùng phiên bản, khác chữ ký, không làm launcher). Bật lại: `pm enable com.fptplay.launcher`.
  Hai lần tắt đầu tiên (`disable-user` rồi `suspend`) bị gỡ sau khởi động lại, kèm
  `lastDisabledCaller: com.fptplay.launcher`; từ lần thứ ba trở đi thì giữ qua 3 lần khởi động. Chưa rõ nguyên nhân:
  không phải do khởi động lại quá sớm (đã thử tắt `com.android.music` rồi `reboot` ngay, vẫn giữ); trong mã của app FPT,
  `FPTBoxService`, `unistallapp`, `system_notification`, `ConsumeCpuService`, `GlobalKeyHandler` không có lệnh bật gói.
  Nếu app FPT cũ lại chạy: đọc `logcat -b all -d` ngay, trước khi nhật ký bị ghi đè.
  Đã thử và bỏ trước đó: shell không có quyền `pm disable` thành phần của gói; `appops RUN_ANY_IN_BACKGROUND`
  bị đặt lại khi khởi động; `am force-stop` chỉ giữ tới lần mở FPT Play kế.
