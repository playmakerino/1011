# Render D:\1011\fingerstyle\ttlt.html from ttlt.tg, in the same layout as mhkcas.html (CSS from laviem.html)
import re, zipfile, html, os
import mk_tg as K
HERE = os.path.dirname(os.path.abspath(__file__))
TG = os.path.join(HERE, 'ttlt.tg')
OUT = os.path.join(HERE, '..', '..', 'ttlt.html')
LAV = os.path.join(HERE, '..', '..', 'laviem.html')
T = K.TUNE; Q = K.Q; S16 = K.S16
DV = {'1': 16, '2': 8, '4': 4, '8': 2, '16': 1}
PC = {n: i for i, n in enumerate('C C# D D# E F F# G G# A A# B'.split())}
ROOT = {'Fmaj7': 'F', 'Fm6': 'F', 'Em7': 'E', 'A7': 'A', 'Dm7': 'D', 'G': 'G', 'Cmaj7': 'C'}
DEG = {'Fmaj7': 'IV', 'Fm6': 'iv', 'Em7': 'iii', 'A7': 'V/ii', 'Dm7': 'ii', 'G': 'V', 'Cmaj7': 'I'}
SKIP = set(range(82, 88))
# color tones: note name -> short label drawn next to the note in the tab
COLOR = {'Fmaj7': {'E': 'maj7'}, 'Fm6': {'G#': 'b3 mượn', 'D': '6th'}, 'Em7': {'D': '7th'},
         'A7': {'C#': '3rd → D', 'G': '7th', 'A#': 'b9'}, 'Dm7': {'C': '7th'}, 'Cmaj7': {'B': 'maj7'}}
NM = 'C C# D D# E F F# G G# A A# B'.split()


LABEL = {
 1: 'lấy đà, chưa có hợp âm',
 2: 'Fmaj7: bass ngân 3 phách, slap phách 4', 3: 'Fm6 (hợp âm mượn): Ab dưới D', 4: 'Em7: D dưới G',
 5: 'A7: giai điệu đi xuống tới A', 6: 'Dm7: A dưới C, D dưới E', 7: 'sheet không ghi hợp âm: giữ Dm7, bass A',
 8: 'Cmaj7: B dưới E tạo màu maj7', 9: 'groove bắt đầu: bass phách 1 & 3, slap phách 2 & 4',
 10: 'Fmaj7: nốt móc kép, chỉ thêm hòa âm phách 3', 11: 'Fm6: Ab dưới D cuối ô', 12: 'Em7: G# cuối ô dẫn về A7',
 13: 'A7: giai điệu C nghịch với C# của hợp âm', 14: 'Dm7: hai câu ngắn A–E–D', 15: 'G: B cuối ô dẫn về C',
 16: 'Cmaj7: kết intro', 17: 'giai điệu nghỉ: quạt Cmaj7, bass E dẫn về F',
 18: 'vào lời: hòa âm phách 1 & 3', 19: 'Fm6: A trong giai điệu, Ab ở dưới', 20: 'Em7: G# dẫn về A7',
 21: 'A7: C# dưới G (quãng 3 cung)', 22: 'Dm7: giai điệu đi xuống F–E–D–C', 23: 'G: F trong giai điệu là 7th',
 24: 'Cmaj7: A trên C là 6th', 25: 'nốt E ngân, bass E dẫn về F', 26: 'Fmaj7: hòa âm cả 4 phách',
 27: 'Fm6: D dưới G, màu m6', 28: 'Em7: câu lặp lần 2', 29: 'A7: giai điệu lên C cao (phím 8)',
 30: 'Dm7: D dưới A, C dưới E', 31: 'G: D dưới F, B dẫn về C', 32: 'Cmaj7: E nối sang ô sau',
 33: 'nốt E ngân, thêm B tạo màu maj7', 34: 'Fmaj7: A dưới nốt C đang ngân', 35: 'Fm6: Ab dưới nốt E ngân',
 36: 'Em7: G, B dưới giai điệu', 37: 'A7: Bb trên cùng là b9', 38: 'Dm7: chặn C và A dưới F',
 39: 'G: B và G dưới nốt E (màu 6th)', 40: 'Cmaj7: quạt C–G–E, ngân hết ô',
 41: 'giai điệu nghỉ cả ô: câu nối E–D–C–B–G',
 42: 'quạt Fmaj7 4 nốt trong chỗ nghỉ', 43: 'Fm6: F dưới C, giai điệu có A', 44: 'Em7: B và E dưới nốt G ngân',
 45: 'A7: C# dưới G', 46: 'Dm7: giai điệu xuống A (dây 3)', 47: 'G: giai điệu xuống G buông, B dẫn về C',
 48: 'Cmaj7: giai điệu nhảy A–E–G–D', 49: 'Cmaj7: G, E dưới C, bass E dẫn về F', 50: 'Fmaj7: G buông ngân từ ô trước',
 51: 'Fm6: kết câu bằng G buông', 52: 'Em7: Bb trong giai điệu (b5)', 53: 'A7: C# dưới E',
 54: 'Dm7: móc kép nhanh, đệm thưa', 55: 'G: C lặp liên tục, B dẫn về C',
 56: 'C cao phím 8: bass E buông, C ở phách 3', 57: 'ngân C cao, chặn G và E (phím 8–9)',
 58: 'đoạn mới: bass nửa nhịp, slap phách 3', 59: 'Fm6: Ab dưới D', 60: 'Em7: C trong giai điệu (b6)',
 61: 'A7: A dưới D, bass ngân', 62: 'Dm7: nhịp chấm dôi, groove trở lại', 63: 'G: B, G dưới F (màu G7)',
 64: 'Cmaj7: B, G dưới E', 65: 'G ngân: Cmaj7 4 nốt, bass E dẫn về F',
 66: 'lời lần cuối: hòa âm cả 4 phách', 67: 'Fm6: D dưới E ở phách 2', 68: 'Em7: D dưới E, G# dẫn về A7',
 69: 'A7: A dưới D ở phách 4', 70: 'Dm7: A dưới D ở phách 2', 71: 'G: G dưới D và C',
 72: 'Cmaj7: C dưới E ở phách 2', 73: 'nốt E ngân, G dưới D', 74: 'Fmaj7: C dưới G và E',
 75: 'Fm6: D dưới G, Ab cuối ô', 76: 'Em7: G# dẫn về A7', 77: 'A7: lên C cao lần cuối',
 78: 'Dm7: A dưới D cuối ô', 79: 'G: G dưới C, B dẫn về C', 80: 'Cmaj7: không nối, giai điệu nghỉ sau ô',
 81: 'đoạn kết: quạt Fmaj7 trong chỗ nghỉ', 88: 'kết bài: quạt Cmaj7, dừng ở C',
}
SECTIONS = {1: 'Lấy đà', 2: 'Intro lần 1 (ô 2–9)', 10: 'Intro lần 2 (ô 10–17)', 18: 'Lời (ô 18–32, đánh 2 lần)',
            33: 'Đoạn B (ô 33–41)', 42: 'Đoạn C (ô 42–57)', 58: 'Volta 2: đoạn D (ô 58–65)',
            66: 'Lời lần cuối (ô 66–80)', 81: 'Kết (ô 81–88)'}

def interval(pc, root):
    return {0: 'root', 1: 'b9', 2: '9th', 3: '3rd', 4: '3rd', 5: '4th', 6: 'b5', 7: '5th', 8: 'b6', 9: '6th', 10: '7th', 11: 'maj7'}[(pc - PC[root]) % 12]

# notes of the first played copy of each sheet bar
x = zipfile.ZipFile(TG).read('content.xml').decode('utf8')
ms = re.findall(r'<TGMeasure>(.*?)</TGMeasure>', x, re.S)
notes = {}
for i, m in enumerate(K.PLAY):
    if m in notes: continue
    mel = {(e['pos'], e['s'], e['f']) for e in K.parse_mel(m)}
    ns = []; mel_done = set()
    for bt in re.findall(r'<TGBeat>(.*?)</TGBeat>', ms[i], re.S):
        t = (int(re.search(r'<preciseStart>(\d+)', bt).group(1)) - Q - i * 16 * S16) // S16
        for vi, (attr, body) in enumerate(re.findall(r'<voice([^>]*)>(.*?)</voice>', bt, re.S)):
            if 'empty="true"' in attr: continue
            for s, tie, f, kids in re.findall(r'<note string="(\d)"( tiedNote="true")? value="(\d+)" velocity="\d+"(/>|><deadNote/></note>)', body):
                n = dict(t=t, s=int(s), f=int(f), tie=bool(tie), dead='deadNote' in kids)
                if vi == 0 and (t, n['s'], n['f']) in mel and t not in mel_done:
                    n['role'] = 'mel'; mel_done.add(t)
                else:
                    n['role'] = 'slap' if n['dead'] else ('bass' if vi == 1 else 'mid')
                ns.append(n)
    assert len(mel_done) == len(mel), m
    notes[m] = ns

X0, DX = 40.5, 21          # one step per 16th note
sy = lambda s: 48 + 18 * (s - 1)

def bar_svg(m):
    o = ['<g class="clef"><line class="tbar" x1="0.75" y1="48" x2="0.75" y2="138"/>'
         '<text class="tclef" x="10" y="80" text-anchor="middle">T</text><text class="tclef" x="10" y="98" text-anchor="middle">A</text>'
         '<text class="tclef" x="10" y="116" text-anchor="middle">B</text></g>']
    o.append(f'<text class="tnum" x="2" y="43">{m}</text>')
    for i, c in enumerate('1+2+3+4+'):
        o.append(f'<text class="{"tcnt" if c != "+" else "tcnt2"}" x="{X0 + DX * 2 * i}" y="164" text-anchor="middle">{c}</text>')
    for s in range(1, 7):
        o.append(f'<line class="tstr" x1="0" y1="{sy(s)}" x2="374" y2="{sy(s)}"/>')
    o.append('<line class="tbar" x1="373.25" y1="48" x2="373.25" y2="138"/>')
    ch = K.CHORD[m]
    if ch and (m == 2 or K.CHORD.get(m - 1) != ch or m in K.SHEET_CH):
        o.append(f'<text class="tch" x="{X0 - 6}" y="30">{html.escape(ch)}<tspan class="tdeg"> {DEG[ch]}</tspan></text>')
    mel_done = set()   # melody color tone labelled once per bar
    for n in notes[m]:
        xx, y = X0 + DX * n['t'], sy(n['s'])
        txt = 'x' if n['dead'] else (f"({n['f']})" if n['tie'] else str(n['f']))
        w = 7 * len(txt) + 4
        cls = n['role']; label = ''
        if cls in ('bass', 'mid') and ch:
            iv = interval((T[n['s'] - 1] + n['f']) % 12, ROOT[ch])
            if cls == 'bass':
                if iv != 'root': cls = 'walk'
                if iv not in ('root', '3rd', '5th'): iv = 'walk'
            label = iv
        nm = NM[(T[n['s'] - 1] + n['f']) % 12]
        if ch in COLOR and nm in COLOR[ch] and not n['dead'] and not n['tie'] and not (cls == 'mel' and nm in mel_done):
            label = COLOR[ch][nm]
            if cls == 'mel': mel_done.add(nm)
        o.append(f'<rect class="tmask" x="{xx - w / 2:.1f}" y="{y - 6.5}" width="{w}" height="13"/>')
        o.append(f'<text class="tnt {cls}" x="{xx}" y="{y + 4.5}" text-anchor="middle">{txt}</text>')
        if label:
            o.append(f'<text class="tiv {cls}" x="{xx + w / 2 + 1:.1f}" y="{y + 3.5}">{label}</text>')
    return f'<svg class="tabsvg" viewBox="0 15 374 157" role="img" aria-label="tab ô {m}">' + ''.join(o) + '</svg>'

lav = open(LAV, encoding='utf8').read()
css = lav[lav.index('<style>'):lav.index('</style>')]
css += '.tnt.slap{fill:var(--slap)}.tiv.mel{fill:var(--mel)}.intro{margin:0 0 12px;font-size:14px;line-height:1.5}\n'
css = css.replace('--mid:#6e8f5a}', '--mid:#6e8f5a;--slap:#475569}')
body = []
for m in range(1, 89):
    if m in SKIP: continue
    if m in SECTIONS:
        if body: body.append('</div>')
        body.append(f'<h3 class="sub">{SECTIONS[m]}</h3><div class="sys">')
    extra = ''
    if m == 81: extra = '<span class="tn">ô 82–87 giống hệt ô 35–40</span>'
    body.append(f'<div class="bar"><div class="tgs"><span class="tk">{html.escape(LABEL[m])}</span>{extra}</div>{bar_svg(m)}</div>')
body.append('</div>')
intro = ('<p class="intro">Không capo, thế C, tempo 116. Giai điệu đánh thấp hơn sheet 1 quãng tám. '
         'Thứ tự: ô 1–57, quay lại ô 17–32, rồi ô 58–88. Ô 82–87 giống hệt ô 35–40 nên không ghi lại.</p>')
page = ('<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<title>Tâm trí lang thang – tab fingerstyle</title>\n' + css + '</style></head>\n<body>\n<div class="page">\n'
        + ''.join(body) + '</div></body></html>')
open(OUT, 'w', encoding='utf8', newline='\r\n').write(page)
print('bars', sum(1 for m in range(1, 89) if m not in SKIP))
