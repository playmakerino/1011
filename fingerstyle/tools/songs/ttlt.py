# Tâm trí lang thang (ttlt): hand-written arrangement, no capo, C shapes, tempo 116. Notes: ttlt.md
# Melody from the sheet (Desktop\ttlt), played one octave below written pitch (guitar convention).
# voice 0 = melody (+ harmony struck with it) + fills in melody rests; voice 1 = bass + slaps.
# Units: 16th notes (16 per bar). Bars keyed by sheet number; PLAY gives the order with the repeat unrolled.
import os
from tablib import SONGS, PAGES, TUNE, Q, X, pitch

TITLE = 'Tâm trí lang thang'; TG_NAME = 'Tam tri lang thang'
CAPO = 0; TEMPO = 116; STEP = Q // 4; BAR = 16
TG = os.path.join(SONGS, 'ttlt.tg'); MELODY_TG = os.path.join(SONGS, 'ttlt_melody.tg')
HTML = os.path.join(PAGES, 'ttlt.html')

NAMES = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
def midi(n):  # 'Bb5' -> written midi, sounding = -12
    acc = -1 if n[1:2] == 'b' else 0
    return 12 * (int(n[-1]) + 1) + NAMES[n[0]] + acc - 12
POS = {55: (3, 0), 57: (3, 2), 59: (2, 0), 60: (2, 1), 62: (2, 3), 64: (1, 0), 65: (1, 1),
       67: (1, 3), 69: (1, 5), 70: (1, 6), 71: (1, 7), 72: (1, 8)}

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
        if k == 'x': ev.append((t, ln, (None, X)))   # string set later: string of the next bass note
        elif k != 'r':
            sf = tuple(map(int, k.split('.'))) if '.' in k else BASS[ch][k]
            ev.append((t, ln, sf))
        t += ln
    assert t == 16, (m, t)
    return ev

for a, b in zip(range(66, 81), range(18, 33)):
    starts = {e['pos'] for e in parse_mel(b) if not e['tie_in'] and e['f'] <= 5}
    A[a] = dict(A[b], h=list(A[b].get('h', [])) + [p for p in (4, 12) if p in starts and p not in A[b].get('h', [])])


def _bars(with_arr):
    bars = [dict(m=m, mel=parse_mel(m), bass=parse_bass(m) if with_arr else []) for m in PLAY]
    # ties: continuation = next melody note (or first note of the next played bar at pos 0), same pitch
    for i, a in enumerate(bars):
        mel = a['mel']
        for j, e in enumerate(mel):
            if not e['tie_out']: continue
            nb = bars[i + 1]['mel'] if i + 1 < len(bars) else []
            nxt = mel[j + 1] if j + 1 < len(mel) else (nb[0] if nb and nb[0]['pos'] == 0 else None)
            if nxt and nxt['p'] == e['p']: nxt['tied'] = True
    out = []
    for a in bars:
        m = a['m']; arr = A[m] if with_arr else {}
        ch = CHORD[m]
        bsound = [(p, p + ln, sf[0]) for p, ln, sf in a['bass'] if sf[1] != X]
        hmap = {}
        for h in arr.get('h', []):
            if isinstance(h, dict): hmap.update(h)
            else: hmap[h] = 'auto'
        harm = {}
        for e in a['mel']:
            if e['pos'] not in hmap: continue
            hs = hmap[e['pos']]
            if hs == 'auto':          # highest candidate below the melody, other string, string not used by the bass
                assert not e['tied'], ('auto harmony on tied note', m, e['pos'])
                busy = {s for a0, b0, s in bsound if a0 < e['pos'] + e['len'] and e['pos'] < b0}
                c = [(s, f) for s, f in HC[ch] if pitch(s, f) < e['p'] and s != e['s'] and s not in busy]
                assert c, ('no auto harmony', m, e['pos'])
                hs = [max(c, key=lambda sf: pitch(*sf))]
            harm[e['pos']] = hs
        for k in hmap:
            if k not in harm: harm[k] = hmap[k]       # reported by the checks (no melody note there)
        out.append(dict(m=m, mel=a['mel'], h=harm, f=arr.get('f', []),
                        b=[(p, ln, [(sf[0] if sf[0] else 6, sf[1])]) for p, ln, sf in a['bass']],
                        vel=(95, 63, 70, 79) if m <= 9 else (95, 72, 79, 85)))
    return out

def bars(): return _bars(True)
def melody_bars(): return _bars(False)

# ---- page ----
DEG = {'Fmaj7': 'IV', 'Fm6': 'iv', 'Em7': 'iii', 'A7': 'V/ii', 'Dm7': 'ii', 'G': 'V', 'Cmaj7': 'I'}
SHOWN = {m: [(0, CHORD[m], DEG[CHORD[m]])] for m in range(2, 89) if CHORD[m] and (m == 2 or CHORD[m - 1] != CHORD[m] or m in SHEET_CH)}
def chord_at(m, t): return CHORD[m]
SKIP = set(range(82, 88))   # = bars 35-40, not drawn again
TAGS = {81: ['ô 82–87 giống hệt ô 35–40']}
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
