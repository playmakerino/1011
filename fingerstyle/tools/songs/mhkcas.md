# Mùa hạ không còn ánh sáng (mhkcas) — ghi chú bản phối

Phong cách dưới đây là của **riêng bài này** (đã chốt qua nhiều lần nghe thử), không áp cho bài khác.

## Thông số
- **Capo 1, thế bấm C** (đổi từ capo 6 thế G ngày 2026-10-04, cùng cao độ thật). Tempo 120 (đúng tempo bài). 24 ô = nửa đầu bài, dừng ngay trước cao trào.
- File gốc người dùng: `Desktop\mhkcas.tg` (capo 1, thế C). Giai điệu ô 19–22 người dùng đã sửa lại → `melody.tg` là bản chuẩn. `melody.tg` vẫn ghi ở thế G capo 6: `mk_tg.py` cộng 5 nửa cung và đặt lại dây/phím theo bảng `MEL`.

## Vòng hợp âm (người dùng gửi, thế C capo 1)
C · G/B · Am7 | Fmaj7 · G · C · A7 | Dm7 · G · G7 · Em7 · Am7 · **A7** | Dm7 | G | Fmaj7 · Fm · Em7 | Am7 · A7 · Dm7 | G

- Ô 13: vòng ghi G#7, nghe tệ dù đổi thế bấm. Người dùng chọn **A7** sau khi nghe so sánh với G#dim7.
- Phải làm **đúng vòng người dùng gửi**, không tự thêm hợp âm (đã bỏ hợp âm lấy đà ở ô 1 và bass đi ở ô 5, 9).

## Phong cách đã chốt
- Pop ballad, sâu lắng, da diết. Không đổi bass root ↔ 5th, không đánh nghịch phách (nghe ra bossa nova).
- Câu 1 (ô 2–9) rất thưa, bass ngân cả ô; dày dần qua câu 2 (10–13), câu 3 (14–17); ô 18–24 dẫn vào cao trào nhưng **không dồn dập**.
- Ô giai điệu nghỉ (5, 9, 13, 17) có câu nối. Ô 17: câu nối đi xuống G–E–D, bass E nối sang F.
- **Slap đúng 1 cái ở phách 3, mỗi ô 2–24**, trên dây của nốt bass kế tiếp (ô 24 không có ô sau, giữ dây 6). Ô đổi hợp âm ở phách 3 (8, 12) → bass mới ở phách 4; ô 21 E7 ở phách 4 cũng có bass E.
- "let ring" ghi một lần ở ô 2, không gắn từng nốt. Không vibrato.
- Luyến: 6 hammer/pull-off có sẵn từ file gốc; slide ở ô 7 (D→B), ô 23 (D→F) và ô 23→24 (E→D). Trang HTML vẽ cung h / p / s, nhưng nhãn ô không nhắc tới luyến.

## Thế bấm capo 1
- Giai điệu lên tới D5–F5 (phím 10–13 dây 1). Ô có G ở phím 10 (7, 11, 24) dùng bass G dây 5 phím 10 (thế chặn); ô 3 G/B bass B dây 6 phím 7. Bass dây buông khi được (Am, Dm, Em) để tay rảnh lên cao.

## Chạy lại
```
python tools/song.py mhkcas         # -> tools/songs/mhkcas.tg + mhkcas.html, in lỗi chồng dây / dãn tay
python tools/song.py mhkcas audit   # in từng nốt, '!' = nốt ngoài hợp âm
```
