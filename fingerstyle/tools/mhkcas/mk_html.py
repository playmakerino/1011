# Render D:\1011\fingerstyle\mhkcas.html from the final .tg, in the same layout as laviem.html
import re, zipfile, html
import os
HERE = os.path.dirname(os.path.abspath(__file__))
TG = os.path.join(HERE, "mhkcas_capo1.tg")
MEL = os.path.join(HERE, "melody.tg")
OUT = os.path.join(HERE, "..", "..", "mhkcas.html")
LAV = os.path.join(HERE, "..", "..", "laviem.html")
T = [64, 59, 55, 50, 45, 40]; Q = 2882880; M = 4*Q; E8 = Q//2
DV = {'1': 8, '2': 4, '4': 2, '8': 1}
PC = {n: i for i, n in enumerate('C C# D D# E F F# G G# A A# B'.split())}

CHORDS = {  # bar -> [(pos, name, root, degree)]
 2:[(0,'C','C','I')], 3:[(0,'G/B','G','V')], 4:[(0,'Am7','A','vi')], 5:[(0,'Am7','A','vi')],
 6:[(0,'Fmaj7','F','IV')], 7:[(0,'G','G','V')], 8:[(0,'C','C','I'),(4,'A7','A','V/ii')], 9:[(0,'Dm7','D','ii')],
 10:[(0,'G','G','V')], 11:[(0,'G7','G','V')], 12:[(0,'Em7','E','iii'),(4,'Am7','A','vi')], 13:[(0,'A7','A','V/ii')],
 14:[(0,'Dm7','D','ii')], 15:[(0,'Dm7','D','ii')], 16:[(0,'G','G','V')], 17:[(0,'G','G','V')],
 18:[(0,'Fmaj7','F','IV'),(4,'Fm','F','iv')], 19:[(0,'Fm','F','iv')], 20:[(0,'Em7','E','iii')],
 21:[(0,'Am7','A','vi'),(6,'A7','A','V/ii')], 22:[(0,'Dm7','D','ii')], 23:[(0,'Dm7','D','ii')], 24:[(0,'G','G','V')],
}
TONES = {'C':'C E G','G/B':'G B D','Am7':'A C E G','Fmaj7':'F A C E','G':'G B D','A7':'A C# E G','Dm7':'D F A C',
         'G7':'G B D F','Em7':'E G B D','Fm':'F G# C'}
LABEL = {
 1:'lấy đà, chưa có hợp âm',
 2:'mở câu: bass C ngân cả ô', 3:'bass B: hợp âm đảo, bấm ở phím 7', 4:'Am7: giai điệu đi xuống',
 5:'giai điệu nghỉ: câu nối nhắc lại G–E', 6:'Fmaj7: E dưới A tạo màu maj7', 7:'G: chặn phím 10, 4 nốt cùng lúc',
 8:'A7 ở phách 3: C# dẫn về Dm7', 9:'giai điệu nghỉ: rải Dm7 đi lên',
 10:'G: A ở trên tạo màu 9th', 11:'G7: quãng F–B tạo độ căng', 12:'Em7 rồi Am7 ở phách 3',
 13:'A7: rải A–C#–E–G, dẫn về Dm7',
 14:'Dm7: hòa âm dày hơn', 15:'câu nối F–E', 16:'G: giai điệu E là 6th', 17:'câu nối đi xuống G–E–D, bass E nối sang F',
 18:'Fmaj7 rồi Fm (hợp âm mượn): Ab trong câu nối', 19:'Fm: D là 6th', 20:'Em7: rải đi lên tới B',
 21:'Am7 rồi A7 ở phách 4', 22:'Dm7: câu nối C–F', 23:'lên phím 13, bass dây buông', 24:'dừng ở G (bậc V), chờ cao trào',
}
SECTIONS = {1:'Lấy đà', 2:'Câu 1 (ô 2–9)', 10:'Câu 2 (ô 10–13)', 14:'Câu 3 (ô 14–17)', 18:'Dẫn vào cao trào (ô 18–24)'}

def interval(note_pc, root):
    return {0:'root',1:'b9',2:'9th',3:'3rd',4:'3rd',5:'4th',6:'b5',7:'5th',8:'b6',9:'6th',10:'7th',11:'maj7'}[(note_pc - PC[root]) % 12]

def chord_at(m, t):
    c = None
    for p, n, r, d in CHORDS.get(m, []):
        if p <= t: c = (n, r)
    return c

def beats(path):
    x = zipfile.ZipFile(path).read('content.xml').decode('utf8')
    out = []
    for mi, mx in enumerate(re.findall(r'<TGMeasure>(.*?)</TGMeasure>', x, re.S)):
        for bt in re.findall(r'<TGBeat>(.*?)</TGBeat>', mx, re.S):
            t = (int(re.search(r'<preciseStart>(\d+)', bt).group(1)) - Q - mi*M) // E8
            for vi, (attr, body) in enumerate(re.findall(r'<voice([^>]*)>(.*?)</voice>', bt, re.S)):
                if 'empty="true"' in attr: continue
                for s, tie, f, _, kids in re.findall(r'<note string="(\d)"( tiedNote="true")? value="(\d+)" velocity="\d+"(/>|>(.*?)</note>)', body):
                    out.append(dict(m=mi+1, t=t, v=vi, s=int(s), f=int(f), tie=bool(tie),
                                    dead='deadNote' in (kids or ''), hammer='hammer' in (kids or ''), slide='slide' in (kids or '')))
    return out

notes = beats(TG)
melset = {(n['m'], n['t'], T[n['s']-1] + n['f'] + 5) for n in beats(MEL) if n['v'] == 0}  # melody.tg is G shapes capo 6
mel_first = set()
for n in notes:   # melody = first note of the v0 beat that matches the user's melody
    if n['v'] == 0 and (n['m'], n['t'], T[n['s']-1] + n['f']) in melset and (n['m'], n['t']) not in mel_first:
        n['role'] = 'mel'; mel_first.add((n['m'], n['t']))
for n in notes:
    if 'role' in n: continue
    n['role'] = 'slap' if n['dead'] else ('bass' if n['v'] == 1 else 'mid')

X0, DX = 40.5, 42
sy = lambda s: 48 + 18 * (s - 1)

def bar_svg(m):
    ns = [n for n in notes if n['m'] == m]
    o = ['<g class="clef"><line class="tbar" x1="0.75" y1="48" x2="0.75" y2="138"/>'
         '<text class="tclef" x="10" y="80" text-anchor="middle">T</text><text class="tclef" x="10" y="98" text-anchor="middle">A</text>'
         '<text class="tclef" x="10" y="116" text-anchor="middle">B</text></g>']
    o.append(f'<text class="tnum" x="2" y="43">{m}</text>')
    for i, c in enumerate('1+2+3+4+'):
        o.append(f'<text class="{"tcnt" if c != "+" else "tcnt2"}" x="{X0 + DX*i}" y="164" text-anchor="middle">{c}</text>')
    for s in range(1, 7):
        o.append(f'<line class="tstr" x1="0" y1="{sy(s)}" x2="374" y2="{sy(s)}"/>')
    o.append('<line class="tbar" x1="373.25" y1="48" x2="373.25" y2="138"/>')
    for p, name, root, deg in CHORDS.get(m, []):
        o.append(f'<text class="tch" x="{X0 + DX*p - 6}" y="30">{html.escape(name)}<tspan class="tdeg"> {deg}</tspan></text>')
    # arcs between consecutive melody notes: h (hammer-on), p (pull-off), s (slide)
    mels = sorted([n for n in ns if n['role'] == 'mel'], key=lambda n: n['t'])
    def arc(x1, x2, y, lab):
        o.append(f'<path class="tslur" d="M{x1},{y} Q{(x1+x2)/2},{y-9} {x2},{y}"/>')
        o.append(f'<text class="tslt" x="{(x1+x2)/2}" y="{y-6}" text-anchor="middle">{lab}</text>')
    for a, b in zip(mels, mels[1:]):
        if a['hammer'] or a['slide']:
            up = T[b['s']-1] + b['f'] > T[a['s']-1] + a['f']
            arc(X0 + DX*a['t'], X0 + DX*b['t'], min(sy(a['s']), sy(b['s'])) - 8, 's' if a['slide'] else ('h' if up else 'p'))
    # slide across the bar line: arc from the left edge of this bar to its first melody note
    prev = sorted([n for n in notes if n['m'] == m - 1 and n['role'] == 'mel'], key=lambda n: n['t'])
    if prev and prev[-1]['slide'] and mels:
        arc(4, X0 + DX*mels[0]['t'], sy(mels[0]['s']) - 8, 's')
    for n in ns:
        x, y = X0 + DX*n['t'], sy(n['s'])
        txt = 'x' if n['dead'] else (f"({n['f']})" if n['tie'] else str(n['f']))
        w = 7 * len(txt) + 4
        cls = n['role']
        label = ''
        if n['role'] in ('bass', 'mid') and not n['dead']:
            c = chord_at(m, n['t'])
            if c:
                pc = (T[n['s']-1] + n['f']) % 12
                iv = interval(pc, c[1])
                if n['role'] == 'bass':
                    if iv != 'root': cls = 'walk'
                    if iv not in ('root', '3rd', '5th'): iv = 'walk'
                    label = iv
                elif n['role'] == 'mid':
                    label = iv
        o.append(f'<rect class="tmask" x="{x - w/2:.1f}" y="{y - 6.5}" width="{w}" height="13"/>')
        o.append(f'<text class="tnt {cls}" x="{x}" y="{y + 4.5}" text-anchor="middle">{txt}</text>')
        if label:
            o.append(f'<text class="tiv {cls}" x="{x + w/2 + 1:.1f}" y="{y + 3.5}">{label}</text>')
    return (f'<svg class="tabsvg" viewBox="0 15 374 157" role="img" aria-label="tab ô {m}">' + ''.join(o) + '</svg>')

lav = open(LAV, encoding='utf8').read()
css = lav[lav.index('<style>'):lav.index('</style>')]
css += ('.tnt.slap{fill:var(--slap)}.tslur{fill:none;stroke:var(--mel);stroke-width:1.2}'
        '.tslt{font:italic 700 10px Arial,sans-serif;fill:var(--mel)}\n')
css = css.replace('--mid:#6e8f5a}', '--mid:#6e8f5a;--slap:#475569}')
body = []
for m in range(1, 25):
    if m in SECTIONS:
        if body: body.append('</div>')
        body.append(f'<h3 class="sub">{SECTIONS[m]}</h3><div class="sys">')
    extra = '<span class="tn">let ring cả bài</span>' if m == 2 else ''
    body.append(f'<div class="bar"><div class="tgs"><span class="tk">{html.escape(LABEL[m])}</span>{extra}</div>{bar_svg(m)}</div>')
body.append('</div>')
page = ('<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<title>Mùa hạ không còn ánh sáng – tab fingerstyle</title>\n' + css + '</style></head>\n<body>\n<div class="page">\n<div class="capo">Capo 1</div>\n'
        + ''.join(body) + '</div></body></html>')
open(OUT, 'w', encoding='utf8', newline='\n').write(page)
print('notes', len(notes), 'mel', sum(n['role'] == 'mel' for n in notes), 'slap', sum(n['role'] == 'slap' for n in notes))
