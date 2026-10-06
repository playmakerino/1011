# Tâm trí lang thang (ttlt): ghi chú bản phối

Đây là phong cách **riêng của bài này**, không dùng cho bài khác.

## Thông số
- Sheet gốc: `Desktop\ttlt\tam_tri_lang_thang_hop_am_trang1-3.jpg` (giọng C, tempo 116, 88 ô).
- Không capo, thế bấm C. Giai điệu đánh thấp hơn nốt viết 1 quãng tám (cách ghi chuẩn cho guitar).
- Thứ tự phát: 1–57, lặp lại 17–32, rồi volta 2 (58–88), tổng 104 ô. Volta 1 kéo dài từ ô 33 tới 57.
- Vòng hợp âm lấy đúng theo sheet. Ô không ghi hợp âm thì giữ hợp âm trước (ô 7 vẫn là Dm7, không thêm G).

## Phong cách (người dùng chọn "groove nhẹ, có slap"; phần đệm theo nguyên lý bản C từ 2026-10-06)
- Groove: bass phách 1 & 3 (root rồi 5th), slap phách 2 & 4, slap trên dây của nốt bass kế tiếp. Bè 1 chỉ có bass + slap; bass ngân tới slap.
- Intro lần 1 (ô 2–9) thưa: bass ngân 3 phách, slap phách 4. Groove vào từ ô 9.
- Đi bass vào hợp âm sau ở móc cuối ô: G → B → C, Cmaj7 → E → F, Em7 → G# → A7.
- Volta 2 ô 58–61: bass nửa nhịp (phách 1, slap phách 3) để tạo tương phản, rồi về groove.
- Ô 56–57 (nốt C cao phím 8): bass E buông thay cho C để không phải dãn tay.
- Phần đệm: "tay trái" viết tay từng ô (`LH` trong `ttlt.py`, người dùng yêu cầu 2026-10-06): thế mở (5th, 9th, 3rd, nốt màu) đi lên rồi ngân; giai điệu dày thì 2–3 nốt, giai điệu ngân thì nhiều hơn; không để nốt đệm trùng nốt giai điệu sắp tới; lời lần cuối (66–80) có móc kép ở phách 1 và nốt đỉnh khác lời lần 1; ô 43 bỏ Ab vì giai điệu có A. Ô 82–87 = 35–40.
- Tay phải (2026-10-06, người dùng yêu cầu): `RH` trong `ttlt.py`, viết tay từng ô — 1–2 nốt đánh cùng nốt giai điệu ở phách chính, dưới giai điệu một quãng 3–6, nốt trong hợp âm; lời lần cuối thêm 1 nốt; ô 82–87 = 35–40; đặt trước tay trái. 195/200 nốt đặt được; ô 46, 55 dùng A, G thay F để không chiếm dây bass D.

## Chạy lại
```
python tools/song.py ttlt         # -> tools/songs/ttlt.tg, ttlt_melody.tg (chỉ giai điệu) + ttlt.html, in lỗi chồng dây / dãn tay
python tools/song.py ttlt audit   # in từng nốt, '!' = nốt ngoài hợp âm
```
