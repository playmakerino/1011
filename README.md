# 1011

Trang GitHub Pages: https://playmakerino.github.io/1011/ (mục lục ở `index.html`).

| Thư mục | Nội dung | Địa chỉ web |
|---|---|---|
| `avocado-tv/` | Avocado TV: trang xem video (`index.html`), dữ liệu `tiktok/` và `drive/`, app Android bọc trang (`android/`, build thành `tv.apk`), script cập nhật dữ liệu (`scripts/`) | `/1011/avocado-tv/` |
| `tre-em/` | Trò chơi cho trẻ: Cân Đĩa, Đồng Hồ, Học Đồng Hồ. App TV "Đồng Hồ" (`android/`, build thành `dong-ho.apk`) mở thẳng Đồng Hồ, có nút chuyển sang Học Đồng Hồ; `tv-nav.js` cho điều khiển bằng remote | `/1011/tre-em/` |
| `fingerstyle/` | Tab guitar fingerstyle | `/1011/fingerstyle/...` |
| `1011-tv/` | Launcher 1011 TV cho hộp FPT Play 650 (không phải trang web; xem `1011-tv/README.md`) | |

`tv.html`, `can-dia.html`, `dong-ho.html`, `hoc-dong-ho.html` ở gốc chỉ là trang chuyển hướng tới chỗ mới, để link cũ
vẫn chạy.

## Tự động (`.github/workflows/`)

- `apk.yml`: mỗi lần `avocado-tv/android/` thay đổi, build `avocado-tv/tv.apk` và commit lại.
- `tiktok.yml`: mỗi ngày cập nhật `avocado-tv/tiktok/` (video mới và ảnh thu nhỏ).
- `apk-dong-ho.yml`: mỗi lần `tre-em/android/` thay đổi, build `tre-em/dong-ho.apk` và commit lại.
- `drive-assets.yml`: khi `avocado-tv/drive/*.json` đổi, chép ảnh và phụ đề vào `avocado-tv/drive/assets/`.
