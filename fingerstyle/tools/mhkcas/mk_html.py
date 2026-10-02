# Render D:\1011\fingerstyle\mhkcas.html from the final .tg, in the same layout as laviem.html
import re, zipfile, html
import os
HERE = os.path.dirname(os.path.abspath(__file__))
TG = os.path.join(HERE, "mhkcas_capo6.tg")
MEL = os.path.join(HERE, "melody.tg")
OUT = os.path.join(HERE, "..", "..", "mhkcas.html")
LAV = os.path.join(HERE, "..", "..", "laviem.html")
T = [64, 59, 55, 50, 45, 40]; Q = 2882880; M = 4*Q; E8 = Q//2
DV = {'1': 8, '2': 4, '4': 2, '8': 1}
PC = {n: i for i, n in enumerate('C C# D D# E F F# G G# A A# B'.split())}

CHORDS = {  # bar -> [(pos, name, root, degree)]
 2:[(0,'G','G','I')], 3:[(0,'D/F#','D','V')], 4:[(0,'Em7','E','vi')], 5:[(0,'Em7','E','vi')],
 6:[(0,'Cmaj7','C','IV')], 7:[(0,'D','D','V')], 8:[(0,'G','G','I'),(4,'E7','E','V/ii')], 9:[(0,'Am7','A','ii')],
 10:[(0,'D','D','V')], 11:[(0,'D7','D','V')], 12:[(0,'Bm7','B','iii'),(4,'Em7','E','vi')], 13:[(0,'E7','E','V/ii')],
 14:[(0,'Am7','A','ii')], 15:[(0,'Am7','A','ii')], 16:[(0,'D','D','V')], 17:[(0,'D','D','V')],
 18:[(0,'Cmaj7','C','IV'),(4,'Cm','C','iv')], 19:[(0,'Cm','C','iv')], 20:[(0,'Bm7','B','iii')],
 21:[(0,'Em7','E','vi'),(6,'E7','E','V/ii')], 22:[(0,'Am7','A','ii')], 23:[(0,'Am7','A','ii')], 24:[(0,'D','D','V')],
}
TONES = {'G':'G B D','D/F#':'D F# A','Em7':'E G B D','Cmaj7':'C E G B','D':'D F# A','E7':'E G# B D','Am7':'A C E G',
         'D7':'D F# A C','Bm7':'B D F# A','Cm':'C D# G'}
LABEL = {
 1:'lấy đà, chưa có hợp âm',
 2:'mở câu: bass G ngân cả ô', 3:'bass F#: hợp âm đảo', 4:'Em7: giai điệu đi xuống',
 5:'giai điệu nghỉ: câu nối nhắc lại D–B', 6:'Cmaj7: B dưới E tạo màu maj7', 7:'D: 3 nốt cùng lúc ở phách 1',
 8:'E7 ở phách 4: G# dẫn về Am7', 9:'giai điệu nghỉ: rải Am7 đi lên',
 10:'D: E ở trên tạo màu 9th', 11:'D7: quãng C–F# tạo độ căng', 12:'hammer-on, pull-off; Em7 ở phách 4',
 13:'E7: rải E–G#–B–D, dẫn về Am7',
 14:'Am7: hòa âm dày hơn', 15:'câu nối C–B', 16:'D: giai điệu B là 6th', 17:'câu nối đi xuống D–B–A, bass B nối sang C',
 18:'Cmaj7 rồi Cm (hợp âm mượn): Eb trong câu nối', 19:'Cm: A là 6th', 20:'Bm7: rải đi lên tới F#',
 21:'Em7 rồi E7 ở phách 4', 22:'Am7: câu nối G–C', 23:'lên phím 8, bass dây buông', 24:'dừng ở D (bậc V), chờ cao trào',
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
                                    dead='deadNote' in (kids or ''), hammer='hammer' in (kids or '')))
    return out

notes = beats(TG)
melset = {(n['m'], n['t'], n['s'], n['f']) for n in beats(MEL) if n['v'] == 0}
mel_first = set()
for n in notes:   # melody = first note of the v0 beat that matches the user's melody
    if n['v'] == 0 and (n['m'], n['t'], n['s'], n['f']) in melset and (n['m'], n['t']) not in mel_first:
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
    # hammer-on / pull-off arcs between consecutive melody notes
    mels = sorted([n for n in ns if n['role'] == 'mel'], key=lambda n: n['t'])
    for a, b in zip(mels, mels[1:]):
        if a['hammer']:
            x1, x2, y = X0 + DX*a['t'], X0 + DX*b['t'], min(sy(a['s']), sy(b['s'])) - 8
            up = T[b['s']-1] + b['f'] > T[a['s']-1] + a['f']
            o.append(f'<path class="tslur" d="M{x1},{y} Q{(x1+x2)/2},{y-9} {x2},{y}"/>')
            o.append(f'<text class="tslt" x="{(x1+x2)/2}" y="{y-6}" text-anchor="middle">{"h" if up else "p"}</text>')
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
        '<title>mhkcas – tab fingerstyle</title>\n' + css + '</style></head>\n<body>\n<div class="page">\n<div class="capo">Capo 6</div>\n'
        + ''.join(body) + '</div></body></html>')
open(OUT, 'w', encoding='utf8', newline='\n').write(page)
print('notes', len(notes), 'mel', sum(n['role'] == 'mel' for n in notes), 'slap', sum(n['role'] == 'slap' for n in notes))
