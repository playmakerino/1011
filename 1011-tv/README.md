# 1011 TV

Màn hình chính kiểu YouTube cho hộp FPT Play 650 (Hisense IP940N, Android TV 14), làm từ
[CleanYourTV](https://github.com/Gathin23/cleanyourtv) (giấy phép MIT, xem `LICENSE`).

- Lưới ô 16:9 có tên app bên dưới, nền #0F0F0F, 4 cột, 3 hàng vừa màn hình.
- Viền trắng nhảy thẳng sang ô được chọn, không trượt.
- App mở nhiều nhất đứng đầu (đếm theo thống kê của Android, 30 ngày gần nhất).
- Bánh răng góc phải: Mạng, Ẩn/hiện ứng dụng (tick ngay trên lưới), Cài đặt.

## Thư mục

| Thư mục | Nội dung |
|---|---|
| `launcher/` | Mã nguồn app (Java). Gói `com.gathin.tvhome`, tên hiển thị "1011 TV". |
| `launcher/app/src/main/res/values/config.xml` | Số cột, số hàng, app ẩn sẵn, đồng hồ bảo vệ màn hình. |
| `tools/` | `tv.py` (kết nối ADB qua mạng), `disable`/`restore` (tắt và bật lại app hệ thống), `b64push.py`, `adb-closed.py`. |
| `fpt-play-650/` | Danh sách app đã tắt trên hộp (`batch1.txt`, `batch2.txt`, `batch3.txt`) và bản sao lưu trước các đợt dọn code. |

## Cài lên hộp

Lần đầu, tạo môi trường Python cho công cụ ADB:

```bash
py -m venv tools/venv
tools/venv/Scripts/pip install -r tools/requirements.txt
```

Build và cài (cần JDK 17 và Android SDK, mặc định lấy ở `%USERPROFILE%\.cleanyourtv-build`):

```powershell
launcher\build-and-install.ps1 -TvHost 192.168.1.2
```

Script cấp quyền đọc thống kê (để sắp theo số lần mở) và quyền vị trí (để đọc tên Wi-Fi), rồi đặt 1011 TV
làm màn hình chính.

## Tắt và bật lại app hệ thống

```bash
TV_HOST=192.168.1.2 bash tools/disable.sh fpt-play-650/batch1.txt
TV_HOST=192.168.1.2 bash tools/restore.sh fpt-play-650/batch1.txt
```

App chỉ bị tắt (`pm disable-user`), không bị gỡ; `restore` bật lại đúng danh sách đó.
