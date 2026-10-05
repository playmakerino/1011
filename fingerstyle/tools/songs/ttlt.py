# Tâm trí lang thang (ttlt): hand-written arrangement, no capo, C shapes, tempo 116. Notes: ttlt.md
# Melody from the sheet (Desktop\ttlt), played one octave below written pitch (guitar convention).
# voice 0 = melody (+ harmony struck with it) + fills in melody rests; voice 1 = bass + slaps.
# Units: 16th notes (16 per bar). Bars keyed by sheet number; PLAY gives the order with the repeat unrolled.
import os
from tablib import SONGS, PAGES, TUNE, Q, X, pitch
import accomp as A

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
# ---- bass line, one entry per bar: 'R:4 x:4 5:4 x:4' (R/5/3 of the chord or s.f explicit, x = slap, r = rest) ----
G4 = 'R:4 x:4 5:4 x:4'            # the groove: bass on 1 & 3, slap on 2 & 4
TO_C = 'R:4 x:4 5:4 x:2 3:2'       # G: B on the last eighth leads to C
TO_F = 'R:4 x:4 5:4 x:2 6.0:2'     # C -> F: E on the last eighth
TO_A = 'R:4 x:4 5:4 x:2 6.4:2'     # Em7 -> A7: G# on the last eighth
# intro first pass (2-9): bass rings 3 beats, slap on 4; part D (58-61): half time; 56-57: open E bass under the high C
BL = {
 1: 'r:16', 2: 'R:12 x:4', 3: 'R:12 x:4', 4: 'R:12 x:4', 5: 'R:12 x:4', 6: 'R:12 x:4',
 7: '5:12 x:4', 8: 'R:12 x:4', 9: G4, 10: G4, 11: G4, 12: TO_A,
 13: G4, 14: G4, 15: TO_C, 16: G4, 17: TO_F, 18: G4,
 19: G4, 20: TO_A, 21: G4, 22: G4, 23: TO_C, 24: G4,
 25: TO_F, 26: G4, 27: G4, 28: TO_A, 29: G4, 30: G4,
 31: TO_C, 32: G4, 33: TO_F, 34: G4, 35: G4, 36: TO_A,
 37: G4, 38: G4, 39: TO_C, 40: G4, 41: TO_F, 42: G4,
 43: G4, 44: TO_A, 45: G4, 46: G4, 47: TO_C, 48: G4,
 49: TO_F, 50: G4, 51: G4, 52: G4, 53: G4, 54: G4,
 55: TO_C, 56: '3:4 x:4 R:4 x:4', 57: '3:4 x:4 3:4 x:4', 58: 'R:8 x:8', 59: 'R:8 x:8', 60: 'R:8 x:8',
 61: 'R:8 x:8', 62: G4, 63: TO_C, 64: G4, 65: TO_F, 66: G4,
 67: G4, 68: TO_A, 69: G4, 70: G4, 71: TO_C, 72: G4,
 73: TO_F, 74: G4, 75: G4, 76: TO_A, 77: G4, 78: G4,
 79: TO_C, 80: G4, 81: G4, 82: G4, 83: TO_A, 84: G4,
 85: G4, 86: TO_C, 87: G4, 88: 'R:4 x:4 5:4 R:4',
}

# ---- accompaniment (bdmt-C principles): written "left hand", one line per bar, placed with accomp.place() ----
# 'pos16:pitch' above the bass (open voicing: 5th, 9th, 3rd, colour tones; rising then held). Busy melody -> fewer
# notes, held melody -> more; no note that lands in unison with the next melody note.
LH = {
 # --- intro, first pass: bass rings 3 beats ---
 2: '2:C3 6:G3 10:A3',            # Fmaj7: 5th, 9th, 3rd under the falling melody
 3: '2:C3 6:Ab3 14:D4',           # Fm6: Ab, then D (6th) under F-G
 4: '2:B2 4:Gb3 6:D4',            # Em7: up to D (7th), held
 5: '2:E3 6:B3 14:G3',            # A7: G (7th) leads on to Dm7
 6: '2:F3 6:A3 10:C4',            # Dm7: rises under the held E
 7: '2:D3 6:F3 10:A3',            # Dm7 over bass A
 8: '2:G3 6:B3 10:D4',            # Cmaj7: maj7 and 9th under the held E
 # --- intro, second pass: groove ---
 9: '2:E3 6:G3 10:B3',            # groove starts
 10: '2:A3 6:C4 10:G3',           # Fmaj7: 3rd, 5th, 9th
 11: '2:C3 6:Ab3 10:C4',          # Fm6
 12: '2:G3 6:B3 10:D4',           # Em7, G# bass at the end
 13: '2:E3 6:Db4 10:G3',          # A7: C# under the high G, G when the melody drops to C
 14: '2:F3 6:A3 10:C4',           # Dm7
 15: '2:B3 6:D4 10:F3',           # G: F (7th) before the B bass
 16: '2:G3 6:B3 10:E3',           # Cmaj7: end of the intro
 17: '2:E3 3:G3 4:B3',            # melody rests: quick rise, then the melody
 # --- verse (played twice) ---
 18: '2:A3 6:C4 10:G3',
 19: '2:Ab3 6:C4 10:G3',
 20: '2:G3 6:B3 10:D4',
 21: '2:B3 6:Db4 10:G3',
 22: '2:A3 6:F3 10:C4',           # Dm7: F under the melody's C
 23: '2:G3 6:B3 10:A3',
 24: '2:E3 6:B3 10:G3',
 25: '2:G3 4:B3',                 # held E: two notes, then the E bass
 26: '2:G3 6:A3 10:C4',           # second cycle: 9th first
 27: '2:C3 6:Ab3 10:C4',
 28: '2:Gb3 6:G3 10:B3',
 29: '2:E3 6:G3 10:Db4',          # melody climbs to C: C# below
 30: '2:F3 6:C4 10:A3',
 31: '2:G3 6:B3 10:F3',           # G7 colour before C
 32: '2:G3 6:B3 14:D4',
 # --- part B: fuller ---
 33: '2:G3 4:B3 6:D4',            # under the held E, rising to D
 34: '2:A3 6:C4 10:G3 14:A3',
 35: '2:G3 6:Ab3 10:C4 14:Ab3',
 36: '2:Gb3 6:G3 10:B3 14:D4',
 37: '2:E3 6:G3 10:Db4 14:B3',    # Bb in the melody = b9
 38: '2:F3 6:A3 10:C4 14:D4',
 39: '2:A3 6:B3 10:G3',
 40: '2:E3 6:G3 10:B3',           # under the long C
 41: '2:G3 4:B3 6:D4 8:E4',       # melody rests the whole bar: Cmaj7 up to E
 # --- part C ---
 42: '2:G3 3:A3 4:C4 10:F3',      # melody rests until beat 2
 43: '2:C3 6:F3 14:D4',           # Fm6 under A in the melody: no Ab here
 44: '2:Gb3 3:B3 10:G3 14:D4',
 45: '2:E3 6:G3 10:B3',           # busy melody
 46: '2:F3 10:E3',                # low melody (A3): two notes
 47: '2:G3 6:B3 10:F3',
 48: '2:G3 6:B3 10:E3',
 49: '2:E3 4:G3',                 # held C, then the E bass
 50: '2:C3 6:A3 10:C4 14:G3',
 51: '2:Ab3 6:C4 10:D4',
 52: '2:B3 6:D4 10:Gb3 14:B3',
 53: '2:E3 6:Db4 10:G3',
 54: '2:F3 6:A3 10:C4',
 55: '2:G3 6:F3 10:B3',           # B leads to C
 56: '2:B3 6:G3 10:D4 14:E4',     # high C at fret 8
 57: '2:G3 4:B3 6:D4 8:E4',       # under the long high C
 # --- part D: half-time bass ---
 58: '2:C3 4:G3 6:A3 10:C4',
 59: '2:C3 4:G3 6:Ab3 14:F3',
 60: '2:B2 4:Gb3 6:G3 10:B3',
 61: '2:E3 4:G3 6:B3',
 62: '2:A3 6:F3 10:C4',           # groove back
 63: '2:A3 6:B3 10:G3',
 64: '2:G3 6:B3 10:D4 14:G3',
 65: '2:G3 6:B3 10:D4',           # held G, then the E bass
 # --- last verse: sixteenth pick-ups, other top notes ---
 66: '2:C3 3:G3 6:A3 10:C4',
 67: '2:C3 3:G3 6:Ab3 10:C4',
 68: '2:B2 3:Gb3 6:G3 10:D4',
 69: '2:E3 3:B3 6:Db4 10:G3',
 70: '2:A3 3:C4 10:F3 14:A3',
 71: '2:G3 3:B3 6:A3 10:F3',
 72: '2:E3 3:G3 6:B3 14:D4',
 73: '2:G3 3:B3 4:D4',
 74: '2:G3 3:A3 6:C4 10:E3',
 75: '2:Ab3 3:C4 10:G3',
 76: '2:Gb3 3:G3 6:B3 10:D4',
 77: '2:E3 3:G3 6:Db4 10:E4',     # last climb to C
 78: '2:A3 3:C4 6:F4 10:C4',
 79: '2:G3 3:B3 10:F3',
 80: '2:E3 3:G3 6:B3',            # no link: the melody rests after this bar
 # --- ending ---
 81: '1:G3 2:A3 3:C4 10:G3',      # melody rests until beat 2
 88: '2:E3 3:G3 4:B3 5:D4',       # last bar: rise, then the melody ends on C
}
for a, b in zip(range(82, 88), range(35, 41)):   # 82-87 = 35-40 (not drawn again)
    LH[a] = LH[b]

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
    for tok in BL[m].split():
        k, ln = tok.split(':'); ln = int(ln)
        if k == 'x': ev.append((t, ln, (None, X)))   # string set later: string of the next bass note
        elif k != 'r':
            sf = tuple(map(int, k.split('.'))) if '.' in k else BASS[ch][k]
            ev.append((t, ln, sf))
        t += ln
    assert t == 16, (m, t)
    return ev

def lh(m): return A.parse_lh(LH.get(m, ''))

DROPPED = []

def melody_bars():
    bars = [dict(m=m, mel=parse_mel(m), h={}, f=[], b=[], vel=(95, 63, 70, 79) if m <= 9 else (95, 72, 79, 85)) for m in PLAY]
    # ties: continuation = next melody note (or first note of the next played bar at pos 0), same pitch
    for i, a in enumerate(bars):
        mel = a['mel']
        for j, e in enumerate(mel):
            if not e['tie_out']: continue
            nb = bars[i + 1]['mel'] if i + 1 < len(bars) else []
            nxt = mel[j + 1] if j + 1 < len(mel) else (nb[0] if nb and nb[0]['pos'] == 0 else None)
            if nxt and nxt['p'] == e['p']: nxt['tied'] = True
    return bars

def bars():
    out = []
    for a in melody_bars():
        m = a['m']; bass, slaps = [], []
        for t, ln, sf in parse_bass(m):
            if sf[1] == X: slaps.append(t)
            else: bass.append((t, sf))
        acc = A.place(m, a['mel'], bass, lh(m), DROPPED)
        bar, d = A.assemble(m, a['mel'], bass, acc, slaps=slaps, vel=(95, 66, 79, 85) if m > 9 else (95, 60, 70, 79))
        DROPPED.extend(d); out.append(bar)
    return out

# ---- page ----
DEG = {'Fmaj7': 'IV', 'Fm6': 'iv', 'Em7': 'iii', 'A7': 'V/ii', 'Dm7': 'ii', 'G': 'V', 'Cmaj7': 'I'}
SHOWN = {m: [(0, CHORD[m], DEG[CHORD[m]])] for m in range(2, 89) if CHORD[m] and (m == 2 or CHORD[m - 1] != CHORD[m] or m in SHEET_CH)}
def chord_at(m, t): return CHORD[m]
SKIP = set(range(82, 88))   # = bars 35-40, not drawn again
TAGS = {81: ['ô 82–87 giống hệt ô 35–40']}
LABEL = {
 1: 'lấy đà, chưa có hợp âm',
 2: 'Fmaj7: bass ngân 3 phách, rải C–G–A đi lên', 3: 'Fm6 (hợp âm mượn): Ab trong phần rải', 4: 'Em7: rải B–F#–D, D (7th) ngân',
 5: 'A7: giai điệu đi xuống tới A', 6: 'Dm7: rải F–A–C dưới nốt E ngân', 7: 'sheet không ghi hợp âm: giữ Dm7, bass A',
 8: 'Cmaj7: rải G–B–D, B là maj7', 9: 'groove bắt đầu: bass phách 1 & 3, slap phách 2 & 4',
 10: 'Fmaj7: rải A–C–G (3rd, 5th, 9th)', 11: 'Fm6: Ab (b3 mượn) trong phần rải', 12: 'Em7: G# cuối ô dẫn về A7',
 13: 'A7: giai điệu C nghịch với C# trong phần rải', 14: 'Dm7: hai câu ngắn A–E–D', 15: 'G: B cuối ô dẫn về C',
 16: 'Cmaj7: kết intro', 17: 'giai điệu nghỉ: rải nhanh E–G–B, bass E dẫn về F',
 18: 'vào lời: rải A–C–G', 19: 'Fm6: A trong giai điệu, Ab trong phần rải', 20: 'Em7: G# dẫn về A7',
 21: 'A7: C# ở phách 2', 22: 'Dm7: giai điệu đi xuống F–E–D–C', 23: 'G: F trong giai điệu là 7th',
 24: 'Cmaj7: A trên C là 6th', 25: 'nốt E ngân, bass E dẫn về F', 26: 'Fmaj7: vòng 2, rải G (9th) trước',
 27: 'Fm6: Ab dưới giai điệu G', 28: 'Em7: câu lặp lần 2', 29: 'A7: giai điệu lên C cao (phím 8)',
 30: 'Dm7: rải F–C–A', 31: 'G: F (7th) rồi bass B dẫn về C', 32: 'Cmaj7: E nối sang ô sau',
 33: 'nốt E ngân, rải G–B–D đi lên', 34: 'đoạn B: rải 4 nốt A–C–G–A', 35: 'Fm6: Ab hai lần trong phần rải',
 36: 'Em7: D (7th) trên đỉnh', 37: 'A7: Bb trong giai điệu là b9', 38: 'Dm7: rải F–A–C–D',
 39: 'G: giai điệu E là 6th, B dẫn về C', 40: 'Cmaj7: B (maj7) trên đỉnh', 41: 'giai điệu nghỉ cả ô: rải Cmaj7 lên tới E',
 42: 'đoạn C: Fmaj7 rải trong chỗ nghỉ', 43: 'Fm6: giai điệu có A nên phần rải bỏ Ab', 44: 'Em7: rải dưới nốt G ngân',
 45: 'A7: giai điệu dày, rải 3 nốt', 46: 'Dm7: giai điệu xuống A (dây 3)', 47: 'G: giai điệu xuống G buông, B dẫn về C',
 48: 'Cmaj7: giai điệu nhảy A–E–G–D', 49: 'Cmaj7: rải rồi thở, bass E dẫn về F', 50: 'Fmaj7: G buông ngân từ ô trước',
 51: 'Fm6: kết câu bằng G buông', 52: 'Em7: Bb trong giai điệu (b5)', 53: 'A7: C# trong phần rải',
 54: 'Dm7: móc kép nhanh, đệm 3 nốt', 55: 'G: C lặp liên tục, B dẫn về C',
 56: 'C cao phím 8: bass E buông, C ở phách 3', 57: 'ngân C cao, rải G–B–D–E',
 58: 'đoạn mới: bass nửa nhịp, slap phách 3', 59: 'Fm6: rải C–G–Ab', 60: 'Em7: C trong giai điệu (b6)',
 61: 'A7: rải E–G–B, bass ngân', 62: 'Dm7: nhịp chấm dôi, groove trở lại', 63: 'G: F trong giai điệu (màu G7)',
 64: 'Cmaj7: B (maj7) trên đỉnh', 65: 'G ngân: rải Cmaj7, bass E dẫn về F',
 66: 'lời lần cuối: phần rải có móc kép ở phách 1', 67: 'Fm6: Ab ở phách 2', 68: 'Em7: G# dẫn về A7', 69: 'A7: C# trong phần rải',
 70: 'Dm7: giai điệu đi xuống', 71: 'G: B dẫn về C', 72: 'Cmaj7: E nối sang ô sau', 73: 'nốt E ngân, bass E dẫn về F',
 74: 'Fmaj7: câu lặp', 75: 'Fm6: Ab dưới giai điệu G', 76: 'Em7: G# dẫn về A7', 77: 'A7: lên C cao lần cuối',
 78: 'Dm7: F trên đỉnh phần rải', 79: 'G: B dẫn về C', 80: 'Cmaj7: không nối, giai điệu nghỉ sau ô',
 81: 'đoạn kết: rải Fmaj7 trong chỗ nghỉ', 88: 'kết bài: rải Cmaj7, dừng ở C',
}
SECTIONS = {1: 'Lấy đà', 2: 'Intro lần 1 (ô 2–9)', 10: 'Intro lần 2 (ô 10–17)', 18: 'Lời (ô 18–32, đánh 2 lần)',
            33: 'Đoạn B (ô 33–41)', 42: 'Đoạn C (ô 42–57)', 58: 'Volta 2: đoạn D (ô 58–65)',
            66: 'Lời lần cuối (ô 66–80)', 81: 'Kết (ô 81–88)'}
