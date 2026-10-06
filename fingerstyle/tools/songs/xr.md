# Xương rồng (xr): ghi chú bản phối

Đây là phong cách **riêng của bài này**, không dùng cho bài khác.

## Thông số
- Sheet gốc: `Desktop\xương rồng.pdf` (sheet piano MuseScore, giọng C / Am, 58 ô, có ghi hợp âm, có D.S. al Coda).
- Người dùng chọn (2026-10-06): đệm sát sheet như bdmt, ghi thẳng 1 lượt theo thứ tự ô trên sheet (không quay lại D.S.), không capo, tempo 70 (người dùng đổi từ 84).
- Lưới móc tam (32 bước/ô, `accomp.BAR = 32`) vì sheet có nhiều nốt 1/32 lấy đà. Chùm 3 nốt 1/32 (ô 2, 6) ghi gần đúng thành 1/32 thường.
- Giai điệu = nốt cao nhất tay phải, thấp hơn nốt viết 1 quãng tám; ô 9–16 thấp hơn 2 quãng tám (người dùng chọn); ô 36–39 giữ nguyên cao độ viết (tay phải xuống thấp ở đó). Nốt hoa mỹ (ô 4, 58) ghi thành 1/32 trước nốt chính. Nốt cuối E = harmonic dây 1 phím 12.
- Tay trái ô 1–4 (sheet ghi khóa Sol) hạ 1 quãng tám để bass nằm ở dây trầm.
- Hợp âm lấy theo ký hiệu trên sheet. Ô 30 sheet ghi B và A thường (không dấu giáng) dưới Fm(add9): chép đúng sheet. Ô 48 hợp âm Gm7 có cụm D–E, lấy Bb.

## Phong cách
- Như bdmt bản C: tay phải dưới giai điệu (`RH`) + tay trái chép nốt (`LH`), đặt bằng `accomp.place()` (span=3, low=4); bè 1 chỉ có bass ngân. Nốt đệm trùng dây với bass ở cùng thời điểm thì bỏ nốt đệm, giữ bass.
- Luyến: `accomp.legato()` mặc định (h/p tối đa 2 phím, từng cặp).

## Chạy lại
```
python tools/song.py xr         # -> tools/songs/xr.tg, xr_melody.tg + ../xr.html
python tools/song.py xr audit
```
