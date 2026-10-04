# Tâm trí lang thang — hand-written arrangement, no capo, C shapes, tempo 116.
# Melody from the sheet (Desktop\ttlt), played one octave below written pitch (guitar convention).
# voice 0 = melody (+ harmony struck with it) + fills in melody rests; voice 1 = bass + slaps.
# Units: 16th notes (16 per bar). Bars keyed by sheet number; PLAY gives the order with the repeat unrolled.
import os, zipfile
HERE = os.path.dirname(os.path.abspath(__file__))
TUNE = [64, 59, 55, 50, 45, 40]
Q = 2882880; S16 = Q // 4; MLEN = 16
X = 'x'
NAMES = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
def midi(n):  # 'Bb5' -> written midi, sounding = -12
    acc = -1 if n[1:2] == 'b' else 0
    return 12 * (int(n[-1]) + 1) + NAMES[n[0]] + acc - 12
POS = {55: (3, 0), 57: (3, 2), 59: (2, 0), 60: (2, 1), 62: (2, 3), 64: (1, 0), 65: (1, 1),
       67: (1, 3), 69: (1, 5), 70: (1, 6), 71: (1, 7), 72: (1, 8)}
pitch = lambda s, f: TUNE[s-1] + f

# ---- melody, written pitch: NOTE/len16, '~' = tied into next note, r/len = rest ----
MEL = {
 1: 'r/12 F5/1 G5/3',
 2: 'G5/4 E5/4 D5/4 C5/1 D5/3',  3: 'D5/4 C5/4 G4/4 F5/1 G5/3',  4: 'G5/4 E5/4 D5/4 C5/1 D5/3',
 5: 'D5/4 C5/4 A4/4 A4/2 B4/2',  6: 'C5/2 C5/2 C5/2 D5/2 E5/6 A4/2',  7: 'G4/6 D5/2 D5/4 C5/4',
 8: 'C5/2 C5/2 C5/2 D5/2 E5/8',  9: 'G5/2 A5/2 E5/2 G5/2 D5/4 E5/4~',
 10: 'E5/4 E5/1 E5/1 F5/2 G5/4 E5/1 E5/1 F5/2',  11: 'G5/4 E5/1 E5/1 F5/2 G5/2 E5/2 D5/4~',
 12: 'D5/4 E5/1 E5/1 F5/2 G5/2 F5/2 F5/2 G5/2',  13: 'G5/2 G5/2 G5/2 A5/2 C5/2 C5/2 D5/2 C5/2',
 14: 'A5/2 E5/2 D5/4 A5/2 E5/2 D5/4',  15: 'G5/1 G5/1 G5/1 G5/1 E5/2 F5/2 G5/2 E5/2 D5/4~',
 16: 'D5/2 A5/2 G5/2 D5/2 D5/2 E5/2 E5/4',
 17: 'r/6 D5/1 D5/1 D5/2 E5/2 D5/2 E5/2',
 18: 'G5/2 G5/2 E5/4 G5/2 G5/2 E5/4',  19: 'G5/2 G5/2 E5/2 A5/2 G5/2 E5/2 D5/4',
 20: 'G5/2 G5/2 E5/4 G5/2 G5/2 E5/4',  21: 'G5/2 G5/2 E5/2 A5/2 G5/2 E5/2 D5/2 E5/2',
 22: 'F5/2 E5/2 D5/2 C5/2 G5/4 E5/4~',  23: 'E5/2 D5/2 D5/2 E5/2 F5/2 E5/2 C5/2 D5/2~',
 24: 'D5/2 A5/2 E5/2 E5/2 G5/2 D5/2 D5/2 E5/2~',  25: 'E5/6 D5/1 D5/1 D5/2 E5/2 D5/2 E5/2',
 26: 'G5/2 G5/2 E5/4 G5/2 G5/2 E5/4',  27: 'G5/2 G5/2 E5/2 A5/2 G5/2 E5/2 D5/4',
 28: 'G5/2 G5/2 E5/4 G5/2 G5/2 E5/4',  29: 'G5/2 A5/2 B5/2 C6/2 B5/2 G5/2 G5/4',
 30: 'A5/2 G5/2 G5/2 A5/2 E5/4 D5/4~',  31: 'D5/2 D5/2 D5/2 E5/2 F5/2 E5/2 C5/2 D5/2~',
 32: 'D5/2 A5/2 E5/2 E5/2 G5/2 D5/2 D5/2 E5/2~',
 33: 'E5/8 r/2 D5/1 D5/1 D5/2 C5/2~',  34: 'C5/4 G5/2 E5/2 G5/2 E5/6~',
 35: 'E5/4 G5/2 E5/2 G5/2 E5/2 D5/4~',  36: 'D5/4 G5/2 E5/2 G5/2 E5/6',
 37: 'Bb5/4 A5/4 E5/2 F5/2 G5/4',  38: 'F5/4 G5/2 E5/2 G5/2 E5/6~',
 39: 'E5/4 G5/2 E5/2 G5/2 E5/2 D5/2 E5/2',  40: 'D5/2 C5/6~ C5/8',  41: 'r/16',
 42: 'r/6 D5/1 D5/1 E5/2 D5/2 C5/2 D5/2',  43: 'E5/2 D5/2 C5/2 A4/2 C5/2 A4/2 A5/2 G5/2~',
 44: 'G5/6 G4/1 G4/1 G5/2 F5/2 E5/2 F5/2',  45: 'G5/2 E5/2 D5/2 C5/2 D5/2 E5/2 D5/2 C5/2~',
 46: 'C5/2 A4/4 C5/2~ C5/2 A4/4 C5/2',  47: 'C5/2 C5/2 C5/2 D5/2 D5/4 G4/2 G4/2',
 48: 'A5/2 E5/2 G5/2 D5/2 E5/2 C5/2 D5/2 A4/2',  49: 'C5/6 C5/1 C5/1 C5/2 D5/2 A4/2 G4/2~',
 50: 'G4/4 G5/2 E5/2 G5/2 E5/6~',  51: 'E5/4 G5/2 E5/2 G5/2 E5/4 G4/2',
 52: 'G5/2 G5/2 G5/2 A5/2 Bb5/2 A5/2 G5/2 G5/2~',  53: 'G5/2 E5/4 G5/2 G5/2 E5/2 D5/2 C5/2',
 54: 'D5/6 E5/1 F5/1 G5/2 D5/1 D5/1~ D5/2 C5/2',  55: 'D5/6 C5/1 C5/1 C5/2 C5/2 C5/2 C5/2',
 56: 'C6/2 G5/2 G5/2 E5/2 G5/2 A5/2 C6/2 C6/2~',  57: 'C6/16',
 58: 'r/2 D5/2 D5/2 E5/2~ E5/2 D5/2 D5/2 G5/2~',  59: 'G5/2 D5/2 D5/2 C5/2 D5/2 E5/2 C5/4~',
 60: 'C5/2 D5/2 D5/2 E5/2~ E5/2 D5/2 D5/2 G5/2~',  61: 'G5/2 D5/2 D5/2 C5/2 D5/2 E5/2 C5/4',
 62: 'F5/3 E5/1~ E5/2 D5/1 C5/1 D5/3 E5/1~ E5/4',  63: 'F5/3 E5/1~ E5/2 D5/1 C5/1 D5/3 E5/1~ E5/4~',
 64: 'E5/2 C5/2 C5/2 D5/2 E5/8',  65: 'E5/2 F5/2 G5/12',
 80: 'D5/2 A5/2 E5/2 E5/2 G5/2 D5/2 D5/2 E5/2',
 81: 'r/4 G5/2 E5/2 G5/2 E5/6~',
 88: 'r/6 D5/1 D5/1 D5/2 C5/2~ C5/4',
}
for a, b in list(zip(range(66, 80), range(18, 32))) + list(zip(range(82, 88), range(35, 41))):
    MEL[a] = MEL[b]

CHORD = {}
cur = None
SHEET_CH = {2: 'Fmaj7', 3: 'Fm6', 4: 'Em7', 5: 'A7', 6: 'Dm7', 8: 'Cmaj7'}
for c0 in (10, 18, 26, 34, 42, 50, 58, 66, 74, 81):   # 8-bar cycles Fmaj7 Fm6 Em7 A7 Dm7 G Cmaj7 (Cmaj7)
    for i, c in enumerate(['Fmaj7', 'Fm6', 'Em7', 'A7', 'Dm7', 'G', 'Cmaj7']):
        SHEET_CH[c0 + i] = c
for m in range(1, 89):
    cur = SHEET_CH.get(m, cur); CHORD[m] = cur      # bars without a symbol keep the previous chord
CHORD[1] = None

# bass: R / 5 / 3 of the chord, or explicit (string, fret)
BASS = {'Fmaj7': {'R': (6, 1), '5': (5, 3), '3': (5, 0)}, 'Fm6': {'R': (6, 1), '5': (5, 3), '3': (6, 4)},
        'Em7': {'R': (6, 0), '5': (5, 2), '3': (6, 3)}, 'A7': {'R': (5, 0), '5': (6, 0), '3': (5, 4)},
        'Dm7': {'R': (4, 0), '5': (5, 0), '3': (6, 1)}, 'G': {'R': (6, 3), '5': (4, 0), '3': (5, 2)},
        'Cmaj7': {'R': (5, 3), '5': (6, 3), '3': (6, 0)}}
# harmony candidates (auto 'H'): highest one below the melody, other string, string not used by bass
HC = {'Fmaj7': [(2, 1), (3, 2), (4, 3), (4, 2)], 'Fm6': [(2, 3), (2, 1), (3, 1), (4, 3), (4, 0)],
      'Em7': [(2, 3), (2, 0), (3, 0), (4, 2), (4, 0)], 'A7': [(2, 2), (3, 0), (4, 2), (3, 2)],
      'Dm7': [(2, 1), (2, 3), (3, 2), (4, 3)], 'G': [(2, 3), (2, 0), (3, 0), (4, 0)],
      'Cmaj7': [(2, 0), (2, 1), (3, 0), (4, 2)]}

# ---- arrangement, one line per bar ----
# b: bass tokens 'R:4 x:4 5:4 x:4' (x = slap, r = rest, s.f = explicit)
# h: melody positions that get one auto chord tone, or {pos: [(s,f),..]} explicit (allowed on a tied note)
# f: fills in melody rests (pos, len, [(s,f)..])
G4 = 'R:4 x:4 5:4 x:4'            # the groove: bass on 1 & 3, slap on 2 & 4
TO_C = 'R:4 x:4 5:4 x:2 3:2'       # G: B on the last eighth leads to C
TO_F = 'R:4 x:4 5:4 x:2 6.0:2'     # C -> F: E on the last eighth
TO_A = 'R:4 x:4 5:4 x:2 6.4:2'     # Em7 -> A7: G# on the last eighth
A = {
 # --- intro, first pass: light, bass rings 3 beats, one slap on 4 ---
 1:  dict(b='r:16'),
 2:  dict(b='R:12 x:4', h=[0, 8]),                      # Fmaj7
 3:  dict(b='R:12 x:4', h=[0, 8]),                      # Fm6: Ab under D, F under the low G
 4:  dict(b='R:12 x:4', h=[0, 8]),                      # Em7
 5:  dict(b='R:12 x:4', h=[0, 8]),                      # A7
 6:  dict(b='R:12 x:4', h=[0, 8]),                      # Dm7
 7:  dict(b='5:12 x:4', h=[0, 8]),                      # Dm7 (no symbol on the sheet), bass A frees string 4
 8:  dict(b='R:12 x:4', h=[0, {8: [(2, 0)]}]),          # Cmaj7, B under E = maj7
 9:  dict(b=G4, h=[0, 8]),                              # groove starts
 # --- intro, second pass ---
 10: dict(b=G4, h=[8]),
 11: dict(b=G4, h=[0, 12]),
 12: dict(b=TO_A, h=[8]),
 13: dict(b=G4, h=[0, 8]),
 14: dict(b=G4, h=[0, 8]),
 15: dict(b=TO_C, h=[0, 8]),
 16: dict(b=G4, h=[2, {12: [(2, 0)]}]),
 17: dict(b=TO_F, f=[(0, 4, [(4, 2), (3, 0), (2, 0)])]),   # Cmaj7 strum in the rest, E -> F
 # --- verse (bars 17-32 are played twice) ---
 18: dict(b=G4, h=[0, 8]),
 19: dict(b=G4, h=[0, 12]),
 20: dict(b=TO_A, h=[0, 8]),
 21: dict(b=G4, h=[0, 8]),
 22: dict(b=G4, h=[0, 8]),
 23: dict(b=TO_C, h=[2, 8]),
 24: dict(b=G4, h=[2, 8]),
 25: dict(b=TO_F, h=[8]),
 26: dict(b=G4, h=[0, 4, 8, 12]),
 27: dict(b=G4, h=[0, 8]),
 28: dict(b=TO_A, h=[0, 8]),
 29: dict(b=G4, h=[0, 12]),
 30: dict(b=G4, h=[0, 8]),
 31: dict(b=TO_C, h=[4, 8]),
 32: dict(b=G4, h=[2, 8]),
 # --- volta 1, part B ---
 33: dict(b=TO_F, f=[(8, 2, [(2, 0)])]),                # B under the held E
 34: dict(b=G4, h=[{0: [(3, 2)]}, 4, 10]),
 35: dict(b=G4, h=[{0: [(3, 1)]}, 8, 12]),
 36: dict(b=TO_A, h=[{0: [(3, 0)]}, {4: [(2, 0)]}, 10]),
 37: dict(b=G4, h=[{0: [(2, 2), (3, 0)]}, {4: [(2, 2)]}, 12]),   # Bb over A7 = b9
 38: dict(b=G4, h=[{0: [(2, 1), (3, 2)]}, 10]),
 39: dict(b=TO_C, h=[{0: [(2, 0), (3, 0)]}, 8]),
 40: dict(b=G4, h=[0, {2: [(3, 0), (4, 2)]}]),
 41: dict(b=TO_F, f=[(0, 4, [(1, 0)]), (4, 2, [(2, 3)]), (6, 2, [(2, 1)]), (8, 4, [(2, 0)]), (12, 4, [(3, 0)])]),  # falling line E D C B G
 # --- volta 1, part C ---
 42: dict(b=G4, f=[(0, 6, [(4, 3), (3, 2), (2, 1), (1, 0)])]),   # Fmaj7 strum in the rest
 43: dict(b=G4, h=[0, {8: [(4, 3)]}]),
 44: dict(b=TO_A, h=[{0: [(2, 0), (4, 2)]}, 8]),       # B and E under the held G
 45: dict(b=G4, h=[0, 8]),
 46: dict(b=G4, h=[{0: [(3, 2)]}]),
 47: dict(b=TO_C, h=[0, 8]),
 48: dict(b=G4, h=[0, 8]),
 49: dict(b=TO_F, h=[{0: [(3, 0), (4, 2)]}]),
 50: dict(b=G4, h=[4, 10]),
 51: dict(b=G4, h=[4, 10]),
 52: dict(b=G4, h=[0, 8]),
 53: dict(b=G4, h=[2, 8]),
 54: dict(b=G4, h=[0, 8]),
 55: dict(b=TO_C, h=[0, 8]),
 56: dict(b='3:4 x:4 R:4 x:4', h=[{0: [(2, 8)]}, {12: [(2, 8)]}]),   # high C at fret 8: open E bass first, C bass under the G
 57: dict(b='3:4 x:4 3:4 x:4', h=[{0: [(2, 8), (3, 9)]}]),
 # --- volta 2, part D: half-time bass, then back to the groove ---
 58: dict(b='R:8 x:8', f=[(0, 2, [(3, 2), (2, 1)])]),
 59: dict(b='R:8 x:8', h=[2, 8]),
 60: dict(b='R:8 x:8', h=[2, 10]),
 61: dict(b='R:8 x:8', h=[2, 12]),
 62: dict(b=G4, h=[{0: [(2, 1), (3, 2)]}, 8]),
 63: dict(b=TO_C, h=[{0: [(2, 0), (3, 0)]}, 8]),
 64: dict(b=G4, h=[{8: [(2, 0), (3, 0)]}]),
 65: dict(b=TO_F, h=[{4: [(2, 0), (3, 0), (4, 2)]}]),
 # --- verse again (66-80 = 18-32, fuller: chord tone on beats 2 and 4 too) ---
 81: dict(b=G4, f=[(0, 4, [(4, 3), (3, 2), (2, 1)])], h=[4]),
 88: dict(b='R:4 x:4 5:4 R:4', f=[(0, 6, [(4, 2), (3, 0), (2, 0)])], h=[{12: [(3, 0), (4, 2)]}]),
}
for a, b in zip(range(82, 88), range(35, 41)):
    A[a] = A[b]

PLAY = list(range(1, 58)) + list(range(17, 33)) + list(range(58, 89))

def parse_mel(m):
    ev, t = [], 0
    for tok in MEL[m].split():
        tie = tok.endswith('~'); tok = tok.rstrip('~')
        n, ln = tok.split('/'); ln = int(ln)
        if n != 'r':
            s, f = POS[midi(n)]
            ev.append(dict(pos=t, len=ln, s=s, f=f, p=midi(n), tie_out=tie, tied=False, tie_in=bool(ev) and ev[-1]['tie_out'] and ev[-1]['pos'] + ev[-1]['len'] == t, name=n))
        t += ln
    assert t == 16, (m, t)
    return ev

def parse_bass(m):
    ch = CHORD[m]; ev, t = [], 0
    for tok in A[m]['b'].split():
        k, ln = tok.split(':'); ln = int(ln)
        if k == 'x': ev.append((t, ln, X))
        elif k != 'r':
            sf = tuple(map(int, k.split('.'))) if '.' in k else BASS[ch][k]
            ev.append((t, ln, sf))
        t += ln
    assert t == 16, (m, t)
    return ev

for a, b in zip(range(66, 81), range(18, 33)):
    starts = {e['pos'] for e in parse_mel(b) if not e['tie_in'] and e['f'] <= 5}
    A[a] = dict(A[b], h=list(A[b].get('h', [])) + [p for p in (4, 12) if p in starts and p not in A[b].get('h', [])])

DUR = {1: (16, 0), 2: (8, 0), 3: (8, 1), 4: (4, 0), 6: (4, 1), 8: (2, 0), 12: (2, 1), 16: (1, 0)}

def note_xml(s, f, vel, tied=False):
    if f == X: return f'<note string="{s}" value="0" velocity="{vel}"><deadNote/></note>'
    return f'<note string="{s}"' + (' tiedNote="true"' if tied else '') + f' value="{f}" velocity="{vel}"/>'

def dur_xml(ln):
    v, d = DUR[ln]
    return f'<duration{" dotted=\"dotted\"" if d else ""} value="{v}"><divisionType enters="1" times="1"/></duration>'

def split_rest(a, b):
    res = []; t = a
    while t < b:
        for k in (16, 8, 4, 2, 1):
            if t % k == 0 and t + k <= b: res.append((t, k)); t += k; break
    return res

def fill_voice(events):
    out = {}; t = 0
    for p, ln, nx in sorted(events, key=lambda e: e[0]):
        assert p >= t, ('overlap', p, t)
        for rt, rk in split_rest(t, p): out[rt] = (rk, '')
        out[p] = (ln, nx); t = p + ln
    for rt, rk in split_rest(t, 16): out[rt] = (rk, '')
    return out

EMPTY = '<voice empty="true"><duration value="4"><divisionType enters="1" times="1"/></duration></voice>'

def build(with_arr):
    bars = [(m, parse_mel(m), parse_bass(m)) for m in PLAY]
    # ties: continuation = first note of next played bar at pos 0, same pitch
    for i, (m, mel, _) in enumerate(bars):
        for j, e in enumerate(mel):
            if not e['tie_out']: continue
            nxt = mel[j + 1] if j + 1 < len(mel) else (bars[i + 1][1][0] if i + 1 < len(bars) and bars[i + 1][1] and bars[i + 1][1][0]['pos'] == 0 else None)
            if nxt and nxt['p'] == e['p']: nxt['tied'] = True
    # slap string = string of the next bass note (same bar, else next played bar)
    flat = [(i, k) for i, (_, _, b) in enumerate(bars) for k in range(len(b))]
    for n, (i, k) in enumerate(flat):
        p, ln, sf = bars[i][2][k]
        if sf != X: continue
        nxt = next((bars[i2][2][k2][2] for i2, k2 in flat[n + 1:] if bars[i2][2][k2][2] != X), (6, 0))
        bars[i][2][k] = (p, ln, (nxt[0], X))
    problems = []; out = []
    for bi, (m, mel, bass) in enumerate(bars):
        a = A[m] if with_arr else dict(b='r:16')
        ch = CHORD[m]
        vm, vh, vb, vs = (95, 63, 70, 79) if m <= 9 else (95, 72, 79, 85)
        if not with_arr: bass = []
        bsound = [(p, p + ln, sf[0]) for p, ln, sf in bass if sf[1] != X]
        ev0 = []; s0 = []
        hmap = {}
        for h in a.get('h', []):
            if isinstance(h, dict): hmap.update(h)
            else: hmap[h] = 'auto'
        bypos = {e['pos']: e for e in mel}
        for k in hmap:
            if k not in bypos: problems.append(f'M{m} harmony at {k}: no melody note')
        for e in mel:
            hs = hmap.get(e['pos'], [])
            if hs == 'auto':
                if e['tied']: problems.append(f'M{m} auto harmony on tied note {e["pos"]}'); hs = []
                else:
                    busy = {s for a0, b0, s in bsound if a0 < e['pos'] + e['len'] and e['pos'] < b0}
                    c = [(s, f) for s, f in HC[ch] if pitch(s, f) < e['p'] and s != e['s'] and s not in busy]
                    if not c: problems.append(f'M{m} no auto harmony at {e["pos"]}'); hs = []
                    else: hs = [max(c, key=lambda sf: pitch(*sf))]
            for s, f in hs:
                if pitch(s, f) >= e['p']: problems.append(f'M{m} harmony above melody at {e["pos"]}')
                if s == e['s']: problems.append(f'M{m} harmony same string as melody at {e["pos"]}')
            fr = [x for x in [e['f']] + [f for _, f in hs] if x > 0]
            if fr and max(fr) - min(fr) > 4: problems.append(f'M{m} stretch at {e["pos"]}')
            nx = note_xml(e['s'], e['f'], vm, e['tied']) + ''.join(note_xml(s, f, vh) for s, f in hs)
            ev0.append((e['pos'], e['len'], nx))
            s0 += [(e['pos'], e['pos'] + e['len'], s) for s in [e['s']] + [s for s, _ in hs]]
        for p, ln, ns in a.get('f', []):
            ev0.append((p, ln, ''.join(note_xml(s, f, vh) for s, f in ns)))
            s0 += [(p, p + ln, s) for s, _ in ns]
        v0 = fill_voice(ev0)
        v1 = fill_voice([(p, ln, note_xml(sf[0], sf[1], vs if sf[1] == X else vb)) for p, ln, sf in bass])
        for a0, b0, x0 in s0:
            for a1, b1, x1 in bsound:
                if x0 == x1 and a0 < b1 and a1 < b0: problems.append(f'M{m} string {x0} clash')
        rows = []
        for t in sorted(set(v0) | set(v1)):
            st = Q + bi * MLEN * S16 + t * S16
            def vx(d):
                if t not in d: return EMPTY
                ln, nx = d[t]
                return f'<voice{"" if nx else " empty=\"false\""}>{dur_xml(ln)}{nx}</voice>'
            txt = ''
            rows.append(f'<TGBeat><preciseStart>{st}</preciseStart>{txt}{vx(v0)}{vx(v1)}</TGBeat>')
        head = '<clef>treble</clef><keySignature>0</keySignature>' if bi == 0 else ''
        out.append('<TGMeasure>' + head + ''.join(rows) + '</TGMeasure>')
    return out, problems

def write(path, measures):
    ch = ('<TGChannel><id>1</id><bank>128</bank><program>0</program><volume>127</volume><balance>64</balance><chorus>0</chorus><reverb>0</reverb><phaser>0</phaser><tremolo>0</tremolo><name>DrumKit</name></TGChannel>'
          '<TGChannel><id>2</id><bank>0</bank><program>25</program><volume>127</volume><balance>64</balance><chorus>0</chorus><reverb>0</reverb><phaser>0</phaser><tremolo>0</tremolo><name>Steel String Acoustic Guitar 1</name></TGChannel>')
    hdr = '<TGMeasureHeader><timeSignature denominator="4" numerator="4"/><tempo>116</tempo></TGMeasureHeader>' * len(measures)
    trk = ('<TGTrack maxFret="29"><name>Track 1</name><channelId>2</channelId><offset>0</offset><color B="0" G="0" R="255"/>'
           + ''.join(f'<TGString>{p}</TGString>' for p in TUNE) + '<TGLyric from="1"/>' + ''.join(measures) + '</TGTrack>')
    xml = ('<?xml version="1.0" encoding="UTF-8" standalone="no"?><TuxGuitarFile><TGVersion major="2" minor="0" revision="1"/><TGSong>'
           '<name>Tam tri lang thang</name><artist/><album/><author/><date/><copyright/><writer/><transcriber/><comments/>'
           + ch + hdr + trk + '</TGSong></TuxGuitarFile>')
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('version.txt', 'TuxGuitar_file_format 2.0'); z.writestr('content.xml', xml.encode('utf8'))

if __name__ == '__main__':
    mm, _ = build(False); write(os.path.join(HERE, 'melody.tg'), mm)
    ma, problems = build(True); write(os.path.join(HERE, 'ttlt.tg'), ma)
    print('\n'.join(problems) or 'no problems', '| played bars:', len(PLAY))
