# Bèo dạt mây trôi (bdmt): ghi chú bản phối

Đây là phong cách **riêng của bài này**, không dùng cho bài khác.

## Thông số
- Sheet gốc: `Desktop\Bèo dạt mây trôi.pdf` (sheet piano Vu Ngoc Tien, giọng C, 61 ô, không ghi hợp âm, không ghi tempo).
- Không capo, thế bấm C, tempo 72. Giai điệu = nốt cao nhất tay phải, đánh thấp hơn nốt viết 1 quãng tám.
- Ô 1 của sheet trống: bắt đầu từ ô 2 (nốt lấy đà C ở phách 3). Ô 61 sheet ghi 8va: đánh không 8va (C phím 8).
- Hợp âm suy từ tay trái piano (người dùng chọn). Đã soát lại từng ô với sheet (2026-10-05): ô 13 nốt cuối là D (cụm A–C–D, Gsus4), ô 52 bass D → E (Dm7 → C/E), ô 58 Dm (không có C). Màu riêng: Gm7–C7 → F (ii–V của IV), Em → E7/G# → Am, Em7 → Ab → Am7, Bm7b5 → E7 → Am.

## Phong cách đã chốt (bản C, 2026-10-06)
- Phần đệm = tay trái piano chép từ sheet (`LH` trong `bdmt.py`), đặt nốt bằng `accomp.place()`: giữ cao độ và thời điểm; nốt dưới E2 nâng 1 quãng tám, nốt ≥ giai điệu hạ 1 quãng tám, nốt trùng bass đang ngân thì bỏ. Giữ 73% nốt tay trái đúng cao độ, 94% đúng tên nốt.
- Bè 1 chỉ có bass (nốt tay trái ở phách 1, chỗ đổi hợp âm, hoặc dưới C3), ngân tới nốt bass sau. Bass cắt sớm ở ô 8, 28, 54 để không dãn tay; ô 61 bass C dây 6 phím 8.
- Tempo 120. G5 ở ô 8, 55 = harmonic dây 3 phím 5 (phím 15 nghe chói).
- Luyến: `accomp.legato()` đổi dây giai điệu trong vùng phím 0–5 để có nhiều cặp cùng dây (1–3 phím → h/p, 4–5 phím → slide); chỉ từng cặp 2 nốt, không chuỗi 3 nốt → 81 h/p + 11 slide, 52 nốt giai điệu đổi dây. Nốt có cụm hòa âm cố định (ô 13, 59, 61) giữ thế bấm.

## Lịch sử
- Bản A (rải móc đơn liên tục theo mẫu tự chế, bass chung bè với nốt rải) và bản B (A thưa lại theo nhịp tay trái, bass ngân) đã bỏ: người dùng thấy bản C "hay hơn hẳn". Lý do đo được: xem `fingerstyle-tab-memory.md` → Nguyên lý soạn phần đệm.

## Chạy lại
```
python tools/song.py bdmt         # -> tools/songs/bdmt.tg, bdmt_melody.tg + ../bdmt.html, in lỗi chồng dây / dãn tay
python tools/song.py bdmt audit   # in từng nốt, '!' = nốt ngoài hợp âm
```

