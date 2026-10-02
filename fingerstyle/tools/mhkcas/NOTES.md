# Mùa hạ không còn ánh sáng (mhkcas) — ghi chú bản phối

Phong cách dưới đây là của **riêng bài này** (đã chốt qua nhiều lần nghe thử), không áp cho bài khác.

## Thông số
- Capo 6, thế bấm G. Tempo 120 (đúng tempo bài). 24 ô = nửa đầu bài, dừng ngay trước cao trào.
- File gốc người dùng: `Desktop\mhkcas.tg` (capo 1, thế C). Giai điệu ô 19–22 người dùng đã sửa lại → `melody.tg` là bản chuẩn.

## Vòng hợp âm (người dùng gửi, thế C capo 1 → thế G capo 6)
C · G/B · Am7 | Fmaj7 · G · C · A7 | Dm7 · G · G7 · Em7 · Am7 · G#7 | Dm7 | G | Fmaj7 · Fm · Em7 | Am7 · A7 · Dm7 | G
→ G · D/F# · Em7 | Cmaj7 · D · G · E7 | Am7 · D · D7 · Bm7 · Em7 · **E7** | Am7 | D | Cmaj7 · Cm · Bm7 | Em7 · E7 · Am7 | D

- Ô 13: vòng ghi G#7 (thế G là D#7), nghe tệ dù đổi thế bấm. Người dùng chọn **E7** (= A7 thế C) sau khi nghe so sánh với D#dim7.
- Phải làm **đúng vòng người dùng gửi**, không tự thêm hợp âm (đã bỏ hợp âm lấy đà ở ô 1 và bass đi ở ô 5, 9).

## Phong cách đã chốt
- Pop ballad, sâu lắng, da diết. Không đổi bass root ↔ 5th, không đánh nghịch phách (nghe ra bossa nova).
- Câu 1 (ô 2–9) rất thưa, bass ngân cả ô; dày dần qua câu 2 (10–13), câu 3 (14–17); ô 18–24 dẫn vào cao trào nhưng **không dồn dập**.
- Ô giai điệu nghỉ (5, 9, 13, 17) có câu nối. Ô 17: câu nối đi xuống D–B–A, bass B nối sang C.
- **Slap đúng 1 cái ở phách 3, mỗi ô 2–24.** Ô đổi hợp âm ở phách 3 (8, 12) → bass mới ở phách 4; ô 21 E7 ở phách 4 cũng có bass E.
- "let ring" ghi một lần ở ô 2, không gắn từng nốt. Không vibrato.
- Luyến: 6 hammer/pull-off có sẵn từ file gốc; slide ở ô 7 (A→F#), ô 23 (A→C) và ô 23→24 (B→A). Trang HTML vẽ cung h / p / s, nhưng nhãn ô không nhắc tới luyến.

## Chạy lại
```
python mk_tg.py     # -> mhkcas_capo6.tg (copy ra Desktop nếu cần)
python audit.py     # in từng nốt, '!' = nốt ngoài hợp âm
python mk_html.py   # -> ../../mhkcas.html
```
