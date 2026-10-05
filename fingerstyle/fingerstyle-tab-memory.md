# Memory: làm trang HTML tab fingerstyle có chú thích

Ghi chú cho lần sau khi làm trang tab có chú thích (ví dụ `fingerstyle.html` trong repo này).

## Sở thích chung
- Viết tiếng Việt, ngắn gọn, dễ hiểu. Không viết đoạn giải thích dài.
- Không dùng emoji. Không dùng ký hiệu khó hiểu; dùng từ như root, 5th, 3rd, walk, maj7, hammer-on, pull-off, slide, slap.
- Không có dark mode (chỉ nền sáng).
- Có 2 phiên bản (capo / không capo) thì xếp trên – dưới, capo ở trên. Tab của bản nào nằm ngay trong khung bản đó.
- Tab cả bài: chỉ làm bản capo nếu không được yêu cầu khác.
- Các mục dưới về màu, cách vẽ, nhãn là quy ước trang tab (dùng cho mọi bài). Phong cách đệm thì riêng từng bài (xem "Quy trình bài mới").
- Không commit/push git trừ khi được yêu cầu. Push phải thẳng lên `main` (xem CLAUDE.md).

## Màu
| Vai trò | Màu |
|---|---|
| Giai điệu | đỏ `#dc2626` |
| Bass phách 1 (root) | xanh đậm `#1e3a8a` |
| Bass phách 3 / walk | xanh nhạt `#3b82f6` |
| Nốt đệm | xanh lá `#2f9e44` |
| Slap (x) | xám đen `#475569` |

## Cách vẽ tab
- Vẽ bằng SVG, **mỗi ô nhịp một hình**. Máy tính 2 ô một hàng, điện thoại mỗi ô một hàng (grid `auto-fill, minmax(min(420px,100%),1fr)`).
- 6 dây ghi `e B G D A E` (e = dây 1 ở trên). Đường chấm dọc mỗi phách, dòng `1 + 2 + 3 + 4` bên dưới.
- Số phím nằm trong ô vuông tô màu theo vai trò.
- Tên hợp âm ở trên, **kèm bậc trong vòng**, ví dụ `Am (vi)`, `Em/G (iii)`, `D/F# (V/V)`.
- Luyến: cung nhỏ nối hai nốt có chữ `h` (hammer-on), `p` (pull-off), `s` (slide). Luyến qua vạch nhịp thì vẽ cung từ mép trái ô sau.
- Chữ nhỏ cạnh nốt bass và nốt đệm cho biết vai trò so với hợp âm, tự tính:
  - `root`, `5th`, `3rd` (bass là 3rd = hợp âm đảo), `walk` (bass không phải root/3rd/5th), `maj7`, `7th`, `9th`.
- Dữ liệu tab lấy **trực tiếp từ file .gp5** để luôn khớp (voice 0: nốt cao nhất = giai điệu, nốt khác = đệm; voice 1: bass, dead note = slap; hiệu ứng hammer/slide của nốt đầu → ký hiệu ở nốt sau).

## Nhãn dưới mỗi ô
- 1 nhãn **đậm** = ý chính riêng của ô, vài chữ. Ví dụ: "mở câu bằng Am (buồn)", "chuẩn bị kết câu: F rồi G", "kết câu, về C", "hợp âm mượn D/F#".
- **Hạn chế "như ô x"**: mỗi ô phải có ý chính riêng.
- Các nhãn thường tự sinh: "đổi hợp âm ở phách 3", "walk bass", "bass là 3rd (hợp âm đảo)", "đệm tạo màu maj7", "slap phách 2 & 4", "hammer-on", "pull-off", "slide".
- Đầu mục có 1 ô chú giải các từ (root, 5th, 3rd, walk, maj7, bậc) và 1 ô "Cách đọc tab". Không lặp lại giải thích ở từng ô.

- Nốt màu: ghi ngay trong tab, chữ nhỏ cạnh nốt giống `root`, `5th` (ví dụ `maj7`, `b3 mượn`, `3rd → D`), giai điệu mỗi ô ghi 1 lần. Không ghi dây/phím, không làm bảng hay đoạn văn riêng. Bảng nhãn: `COLOR` trong `tools/tablib.py`. laviem (trang làm tay): chạy `python tools/color_tags.py`.
- Đầu trang: chỉ ghi capo nếu có capo. Không đoạn giới thiệu, không ghi "let ring".

- Slap: chỉ 1 dây, là dây của nốt bass kế tiếp (áp dụng mọi bài).

## Cấu trúc mục tab cả bài
- Chia theo đoạn: lấy đà, lời 1, điệp khúc 1, điệp khúc 2 và kết.
- Đoạn lặp giống hệt (ví dụ lời 2 chỉ thêm slap phách 4) thì **không ghi lại**, chỉ nói một câu ở phần giới thiệu.

## Kiểm tra trước khi giao
- So cao độ từng nốt giai điệu (cộng capo) với sheet gốc: phải khớp 100%.
- Không có nốt trùng dây giữa giai điệu/đệm và bass tại cùng thời điểm.
- Tab trong HTML khớp vị trí với file .gp5.
- Chụp màn hình máy tính và điện thoại (390px); `document.documentElement.scrollWidth` phải bằng độ rộng màn hình.

## Giao file
- Ghi đè `D:\1011\fingerstyle\guide.html` (tab cả bài tách riêng ở `fingerstyle\laviem.html`, bài mới thêm vào `fingerstyle\tabs.html`) (dùng CRLF) và bản trên Desktop `fingerstyle_khong_can_tab.html` nếu có.

## Quy trình bài mới (rút ra từ bài mhkcas)
- Phong cách đệm (mật độ, slap, bass, độ dồn) là **riêng từng bài**, không phải gu chung. Mỗi bài ghi phong cách đã chốt vào `tools/songs/<bài>.md`. Bài mới: hỏi người dùng muốn vibe gì, đừng bê phong cách bài cũ.
- Xin **vòng hợp âm gốc** ngay từ đầu. Hợp âm đoán từ giai điệu sai nhiều chỗ.
- Làm file **.tg** cho người dùng nghe duyệt trước, xong mới làm HTML.
- **Viết tay từng ô** (dữ liệu từng ô trong script), không sinh đệm bằng một quy tắc lặp cả bài: nghe máy móc, không có chỗ thưa/dày, câu nối, độ dồn.
- Phân vân giữa vài hợp âm cho 1 ô → làm vài file chỉ khác đúng ô đó để người dùng nghe chọn, rồi xóa file thử.
- Sao lưu file trước mỗi lần ghi đè. Sửa script bằng file .py (Write), không dùng `sed`/`python -c` với đường dẫn Windows (dấu `\` làm hỏng lệnh).
- Sau khi xong: `python tools/song.py <bài>` báo chồng dây, dãn tay; `python tools/song.py <bài> audit` in nốt ngoài hợp âm.

## File .tg (TuxGuitar 2.0)
- Zip gồm `version.txt` + `content.xml`. Capo = `<offset>` của track (đọc trước khi đoán giọng).
- Tick: phách đen = 2882880, ô 1 bắt đầu ở 2882880. Mỗi `<TGBeat>` có 2 `<voice>`; `empty="true"` = bè không bắt đầu ở phách này; `empty="false"` không có nốt = dấu lặng. Mỗi bè phải đủ phách.
- Hiệu ứng là thẻ con của `<note>`: `<hammer/>` (nốt đầu của hammer/pull), `<deadNote/>` (slap), `<letRing/>`, `<vibrato/>`. Nối: thuộc tính `tiedNote="true"`. Chữ cho phách: `<text>…</text>` ngay sau `<preciseStart>`.
- `<letRing/>` gắn từng nốt sẽ hiện "lr" khắp tab → ghi chữ "let ring" một lần ở đầu bài.
- Bè 0 = giai điệu + nốt hòa âm đánh cùng (cùng trường độ) + câu nối trong chỗ giai điệu nghỉ; bè 1 = bass ngân dài + slap. Bass để chung bè với nốt đệm thì bị cắt khi phát lại.
- Không kiểm tra được bằng TuxGuitar trên máy (Java đi kèm thiếu trình biên dịch); tên thẻ lấy từ `tuxguitar-lib.jar` (`app/tuxguitar/io/tg/TGStream.class`).

## Công cụ
- `tools/tablib.py`: phần chung (ghi .tg, kiểm tra chồng dây/dãn tay, vẽ trang tab theo bố cục và CSS của `laviem.html`, audit).
- `tools/songs/<bài>.py`: chỉ dữ liệu của bài (giai điệu, bản phối viết tay từng ô, nhãn, hợp âm); `<bài>.md`: phong cách; `<bài>.tg`: file xuất. Danh sách trường cần có ở đầu `tools/song.py`. Bài mới: copy `songs/ttlt.py` (giai điệu gõ bằng chữ, lưới móc kép) hoặc `songs/mhkcas.py` (giai điệu đọc từ .tg của người dùng, lưới móc đơn) rồi sửa dữ liệu.
- Chạy: `python tools/song.py <bài>` (thêm `audit` để in nốt ngoài hợp âm).
- Skill `fingerstyle-tab-sungha-style` không dùng (xuất .gp5 bằng pyguitarpro, máy không có; mặc định khác cách làm ở đây).
