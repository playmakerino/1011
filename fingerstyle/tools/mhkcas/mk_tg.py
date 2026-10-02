# Hand-written arrangement, capo 6, G shapes. Melody taken from the user's edited file.
# voice 0 = melody (+ harmony notes struck with it) + fills in melody rests
# voice 1 = bass (sustained) + slaps
import re, zipfile
import os
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "melody.tg")
OUT = os.path.join(HERE, "mhkcas_capo6.tg")
TUNE = [64, 59, 55, 50, 45, 40]
Q = 2882880; E8 = Q // 2; MLEN = 4 * Q
X = 'x'  # slap (dead note)

z = zipfile.ZipFile(SRC)
xml = z.read('content.xml').decode('utf8'); ver = z.read('version.txt')
measures = re.findall(r'<TGMeasure>(.*?)</TGMeasure>', xml, re.S)
DUR = {1: (8, 0), 2: (4, 0), 3: (4, 1), 4: (2, 0), 6: (2, 1), 8: (1, 0)}
INV = {(v, d): k for k, (v, d) in DUR.items()}
pitch = lambda s, f: TUNE[s-1] + f

mel = []
for mi, m in enumerate(measures):
    ev = []
    for b in re.findall(r'<TGBeat>(.*?)</TGBeat>', m, re.S):
        st = int(re.search(r'<preciseStart>(\d+)', b).group(1))
        v0 = re.search(r'<voice[^>]*>(.*?)</voice>', b, re.S).group(1)
        n = re.search(r'<note([^>]*?)(/>|>(.*?)</note>)', v0, re.S)
        if not n: continue
        d = re.search(r'<duration( dotted="dotted")? value="(\d+)"', v0)
        s = int(re.search(r'string="(\d)"', n.group(1)).group(1)); f = int(re.search(r'value="(\d+)"', n.group(1)).group(1))
        ev.append(dict(pos=(st - Q - mi*MLEN)//E8, len=INV[(int(d.group(2)), 1 if d.group(1) else 0)],
                       s=s, f=f, hammer='<hammer/>' in (n.group(3) or ''), tied='tiedNote' in n.group(1)))
    mel.append(ev)
for e in mel[11]:
    if e['pos'] == 2: e['s'], e['f'] = 2, 5   # E4 on s2f5 so E->D pull-off stays on one string

# h: harmony notes added to the melody note starting at pos
# f: fills (pos, len, notes) inside melody rests (voice 0)
# b: voice 1 (pos, len, notes)
A = {
 # --- Verse: very sparse, bass rings the whole bar ---
 1:  dict(h={}, f=[], b=[]),
 2:  dict(h={0:[(3,0)]}, f=[], b=[(0,4,[(6,3)]),(4,4,[(5,X)])]),                                   # G
 3:  dict(h={0:[(2,3)], 3:[(3,2)]}, f=[(7,1,[(2,3)])], b=[(0,4,[(6,2)]),(4,4,[(5,X)])]),            # D/F#
 4:  dict(h={0:[(3,0)], 3:[(4,2)]}, f=[(7,1,[(3,0)])], b=[(0,4,[(6,0)]),(4,4,[(5,X)])]),            # Em7
 5:  dict(h={}, f=[(1,1,[(4,2)]),(2,1,[(3,0)]),(3,2,[(2,3)]),(5,2,[(2,0)])],          # Em7: echo D->B of bar 4
          b=[(0,4,[(6,0)]),(4,4,[(5,X)])]),
 6:  dict(h={0:[(4,2)], 3:[(2,0)]}, f=[], b=[(0,4,[(5,3)]),(4,4,[(6,X)])]),                         # Cmaj7
 7:  dict(h={0:[(2,3),(3,2)], 4:[(2,3)]}, f=[], b=[(0,4,[(4,0)]),(4,4,[(6,X)])]),                   # D
 8:  dict(h={0:[(2,0),(3,0)]}, f=[(6,1,[(3,1)]),(7,1,[(4,2)])],                       # G -> E7 (G# leads to Am)
          b=[(0,4,[(6,3)]),(4,2,[(5,X)]),(6,2,[(6, 0)])]),
 9:  dict(h={}, f=[(1,1,[(4,2)]),(2,1,[(3,2)]),(3,3,[(2,1)])], b=[(0,4,[(5,0)]),(4,4,[(6,X)])]),     # Am7
 # --- a little more motion ---
 10: dict(h={0:[(2,3),(3,2)]}, f=[(4,1,[(3,2)]),(5,1,[(2,3)])], b=[(0,4,[(4,0)]),(4,4,[(6,X)])]),   # D (add9)
 11: dict(h={0:[(2,1),(3,2)], 3:[(2,1)]}, f=[(7,1,[(3,2)])], b=[(0,4,[(4,0)]),(4,4,[(6,X)])]),      # D7 (C-F# tritone)
 12: dict(h={1:[(3,4)], 3:[(3,2)]}, f=[(7,1,[(3,0)])],                                # Bm7 -> Em7
          b=[(0,4,[(5,2)]),(4,2,[(6,X)]),(6,2,[(6, 0)])]),
 13: dict(h={}, f=[(1,1,[(4,2)]),(2,1,[(3,1)]),(3,1,[(2,0)]),(4,2,[(4,0)])],          # E7 (= A7 in C shapes)
          b=[(0,4,[(6,0)]),(4,4,[(5,X)])]),
 # --- second phrase: fuller ---
 14: dict(h={0:[(3,2),(4,2)], 3:[(3,0)]}, f=[], b=[(0,4,[(5,0)]),(4,4,[(6,X)])]),     # Am7
 15: dict(h={0:[(4,2)]}, f=[(5,1,[(2,1)]),(6,1,[(2,0)])], b=[(0,4,[(5,0)]),(4,4,[(6,X)])]),  # Am7, fill C-B
 16: dict(h={0:[(3,2)]}, f=[], b=[(0,4,[(4,0)]),(4,4,[(6,X)])]),         # D6
 17: dict(h={}, f=[(2,1,[(2,3)]),(3,1,[(2,0)]),(4,2,[(3,2)])],                        # D: falling line D-B-A into melody G
          b=[(0,4,[(4,0)]),(4,2,[(6,X)]),(6,2,[(5, 2)])]),                                                # bass D then B -> C of bar 18
 # --- pre-chorus: bass on 1 and 3, slap on 2 and 4 every bar ---
 18: dict(h={0:[(2,0),(3,0)]}, f=[(4,1,[(4,1)]),(5,1,[(3,0)]),(6,1,[(2,1)])],         # Cmaj7 -> Cm (Eb in the fill)
          b=[(0,4,[(5,3)]),(4,4,[(6,X)])]),
 19: dict(h={0:[(3,5)], 2:[(4,5)], 6:[(2,4)]}, f=[],                                  # Cm (A = 6th)
          b=[(0,4,[(5,3)]),(4,4,[(6,X)])]),
 20: dict(h={0:[(3,2)]}, f=[(4,1,[(4,4)]),(5,1,[(3,2)]),(6,1,[(2,3)])],               # Bm7
          b=[(0,4,[(5,2)]),(4,4,[(6,X)])]),
 21: dict(h={0:[(2,0),(3,0)], 2:[(3,0)], 6:[(3,1)]}, f=[],                            # Em7 -> E7 (G# on beat 4)
          b=[(0,4,[(6,0)]),(4,2,[(5,X)]),(6,2,[(6,0)])]),
 22: dict(h={0:[(3,2),(4,2)]}, f=[(4,1,[(3,0)]),(5,1,[(2,1)])],                       # Am7
          b=[(0,4,[(5,0)]),(4,4,[(6,X)])]),
 23: dict(h={0:[(2,1),(3,2)], 2:[(2,5)], 3:[(2,5)], 5:[(2,5)]}, f=[],                 # Am7 up high, open A bass
          b=[(0,4,[(5,0)]),(4,4,[(6,X)])]),
 24: dict(h={0:[(2,3),(3,2)]}, f=[(4,1,[(3,2)]),(5,1,[(2,3)]),(6,2,[(1,2)])],         # D, rising fill D-F#
          b=[(0,4,[(4,0)]),(4,4,[(6,X)])]),
}
VEL = {}  # (melody, harmony/fill, bass, slap) per bar
for m in range(1, 25):
    VEL[m] = (95, 63, 63, 79) if m <= 9 else (95, 79, 79, 79) if m <= 13 else (111, 79, 79, 95) if m <= 17 else (111, 79, 79, 79)

def note_xml(s, f, vel, tied=False, hammer=False):
    if f == X: return f'<note string="{s}" value="0" velocity="{vel}"><deadNote/></note>'
    a = f'<note string="{s}"' + (' tiedNote="true"' if tied else '') + f' value="{f}" velocity="{vel}"'
    return a + ('><hammer/></note>' if hammer else '/>')

def dur_xml(ln):
    v, d = DUR[ln]
    return f'<duration{" dotted=\"dotted\"" if d else ""} value="{v}"><divisionType enters="1" times="1"/></duration>'

def split_rest(a, b):
    res = []; t = a
    while t < b:
        for k in (8, 4, 2, 1):
            if t % k == 0 and t + k <= b: res.append((t, k)); t += k; break
    return res

def fill_voice(events):  # events: list of (pos, len, xml) -> {pos: (len, xml)} with rests
    out = {}; t = 0
    for p, ln, nx in sorted(events):
        assert p >= t, ('overlap', p, t)
        for rt, rk in split_rest(t, p): out[rt] = (rk, '')
        out[p] = (ln, nx); t = p + ln
    for rt, rk in split_rest(t, 8): out[rt] = (rk, '')
    assert sum(k for k, _ in out.values()) == 8
    return out

EMPTY = '<voice empty="true"><duration value="4"><divisionType enters="1" times="1"/></duration></voice>'
out_measures = []; problems = []
for mi in range(24):
    m = mi + 1; a = A[m]; vm, vh, vb, vs = VEL[m]
    ev0 = []; sounding0 = []; sounding1 = []
    for e in mel[mi]:
        hs = a['h'].get(e['pos'], [])
        for s, f in hs:
            if pitch(s, f) >= pitch(e['s'], e['f']): problems.append(f'M{m} harmony above melody at {e["pos"]}')
            if s == e['s']: problems.append(f'M{m} harmony same string as melody at {e["pos"]}')
            frets = [x for x in [f, e['f']] if x > 0]
            if frets and max(frets) - min(frets) > 4: problems.append(f'M{m} stretch at {e["pos"]}')
        nx = note_xml(e['s'], e['f'], vm, e['tied'], e['hammer']) + ''.join(note_xml(s, f, vh) for s, f in hs)
        ev0.append((e['pos'], e['len'], nx))
        sounding0 += [(e['pos'], e['pos'] + e['len'], s) for s in [e['s']] + [s for s, _ in hs]]
    for p, ln, ns in a['f']:
        ev0.append((p, ln, ''.join(note_xml(s, f, vh) for s, f in ns)))
        sounding0 += [(p, p + ln, s) for s, _ in ns]
    for k in a['h']:
        if k not in [e['pos'] for e in mel[mi]]: problems.append(f'M{m} harmony at {k} has no melody note')
    v0 = fill_voice(ev0)
    ev1 = []
    for p, ln, ns in a['b']:
        ev1.append((p, ln, ''.join(note_xml(s, f, vs if f == X else vb) for s, f in ns)))
        sounding1 += [(p, p + ln, s) for s, f in ns if f != X]
    v1 = fill_voice(ev1)
    for a0, b0, s0 in sounding0:          # same string sounding in both voices at once
        for a1, b1, s1 in sounding1:
            if s0 == s1 and a0 < b1 and a1 < b0: problems.append(f'M{m} string {s0} clash v0[{a0},{b0}) v1[{a1},{b1})')
    rows = []
    for t in sorted(set(v0) | set(v1)):
        st = Q + mi * MLEN + t * E8
        def vx(d):
            if t not in d: return EMPTY
            ln, nx = d[t]
            return f'<voice{"" if nx else " empty=\"false\""}>{dur_xml(ln)}{nx}</voice>'
        txt = '<text>let ring</text>' if (mi, t) == (1, 0) else ''
        rows.append(f'<TGBeat><preciseStart>{st}</preciseStart>{txt}{vx(v0)}{vx(v1)}</TGBeat>')
    head = '<clef>treble</clef><keySignature>0</keySignature>' if mi == 0 else ''
    out_measures.append('<TGMeasure>' + head + ''.join(rows) + '</TGMeasure>')

print('\n'.join(problems) or 'no problems')
i0 = xml.index('<TGMeasure>'); i1 = xml.rindex('</TGMeasure>') + len('</TGMeasure>')
new = xml[:i0] + ''.join(out_measures) + xml[i1:]
new = re.sub(r'<offset>\d+</offset>', '<offset>6</offset>', new, count=1)
new = re.sub(r'<tempo>\d+</tempo>', '<tempo>120</tempo>', new)
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as zo:
    zo.writestr('version.txt', ver); zo.writestr('content.xml', new.encode('utf8'))
