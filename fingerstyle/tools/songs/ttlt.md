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
- Phần đệm: "tay trái" thế mở 1–5–9–3 trên root (`VO` trong `ttlt.py`), đặt bằng `accomp.place()`. Nhịp theo đoạn (`LH`): intro lần 1 ba nốt đi lên rồi ngân; lời: 5th, 3rd rồi 9th ngân; đoạn B, C: bốn nốt lên tới nốt màu; đoạn D: chạy lên rồi ngân; ô Cmaj7 thứ hai của mỗi vòng 8 ô thì thưa lại; ô 41 rải Cmaj7 lên tới B.
- Lưu ý: nhịp đệm đang viết theo mẫu từng đoạn (+ vài ô sửa tay), chưa viết tay đủ từng ô.

## Chạy lại
```
python tools/song.py ttlt         # -> tools/songs/ttlt.tg, ttlt_melody.tg (chỉ giai điệu) + ttlt.html, in lỗi chồng dây / dãn tay
python tools/song.py ttlt audit   # in từng nốt, '!' = nốt ngoài hợp âm
```
