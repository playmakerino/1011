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
- **Phần đệm theo nguyên lý bản C (2026-10-06, người dùng chọn):** "tay trái" tự viết từng ô (`LH` trong `mhkcas.py`): thế mở 1–5–9–3 đi lên rồi ngân (Fmaj7 = F2–C3–G3–A3 + E, Am7 = A2–E3–B3–C4), đặt bằng `accomp.place()`. Bè 1 chỉ có bass, ngân tới slap.
- Câu 1 (ô 2–9) thưa; ô giai điệu nghỉ (5, 9, 13) rải tiếp đi lên; dày dần ở câu 3; ô 18–24 không dồn dập.
- **Slap đúng 1 cái ở phách 3, mỗi ô 2–24**, trên dây của nốt bass kế tiếp. Ô đổi hợp âm (8, 12, 17, 21) có bass mới ở phách 4.
- Hợp âm và vị trí bass giữ như bản trước; nốt đệm thêm 9th (D trong C, A trong G, B trong Am7, G trong Fmaj7, F# trong Em7, E trong Dm7).
- Luyến: 6 hammer/pull-off có sẵn từ file gốc; slide ở ô 7 (D→B), ô 23 (D→F) và ô 23→24 (E→D).
- Bản trước (nốt hòa âm + câu nối viết tay, bass + slap chung bè) đã thay bằng bản này.

## Thế bấm capo 1
- Giai điệu lên tới D5–F5 (phím 10–13 dây 1). Ô có G ở phím 10 (7, 11, 24) dùng bass G dây 5 phím 10 (thế chặn); ô 3 G/B bass B dây 6 phím 7. Bass dây buông khi được (Am, Dm, Em) để tay rảnh lên cao.

## Chạy lại
```
python tools/song.py mhkcas         # -> tools/songs/mhkcas.tg + mhkcas.html, in lỗi chồng dây / dãn tay
python tools/song.py mhkcas audit   # in từng nốt, '!' = nốt ngoài hợp âm
```
