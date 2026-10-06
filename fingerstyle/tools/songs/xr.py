# Xương rồng (xr): no capo, tempo 84. Notes: xr.md
# Melody = top line of the piano sheet (Desktop\xương rồng.pdf), one octave below written pitch (bars 36-39: as written,
# the right hand goes down there), re-fingered for h/p pairs (accomp.legato). Chords = the sheet's chord symbols.
# Accompaniment = the piano right hand under the melody (RH) + the left hand note for note (LH), placed with accomp.place().
# Bass = the left-hand note on beat 1, on a chord change, or below C3; voice 1 = bass only, ringing.
# Units: 32nd notes (32 per bar; the sheet has 32nd pick-ups). Played once straight through (no D.S.), 58 bars.
import os
from tablib import SONGS, PAGES, Q, TUNE
import accomp as A

TITLE = 'Xương rồng'; TG_NAME = 'Xuong rong'
CAPO = 0; TEMPO = 70; STEP = Q // 8; BAR = 32
A.BAR = BAR
TG = os.path.join(SONGS, 'xr.tg'); MELODY_TG = os.path.join(SONGS, 'xr_melody.tg')
HTML = os.path.join(PAGES, 'xr.html')

SHIFT = {m: 0 for m in (36, 37, 38, 39)}      # octave shift of the written right hand; default -12
SHIFT.update({m: -24 for m in range(9, 17)})   # user: bars 9-16 one more octave down
def shift(m): return SHIFT.get(m, -12)

def pos(p):          # default fingering of a played pitch: low frets, high strings
    c = [(s, p - TUNE[s - 1]) for s in range(1, 7) if 0 <= p - TUNE[s - 1] <= 15]
    return min(c, key=lambda sf: (max(0, sf[1] - 5), sf[0]))

# ---- melody, written pitch: NOTE/len32, '~' = tied into next note, r/len = rest ----
MEL = {
 1: 'E6/4 F6/4 E6/4 A5/4 C6/12 C6/2 D6/2',
 2: 'E6/4 F6/4 E6/4 Ab5/4 C6/8 D6/6 Db6/1 C6/1',
 3: 'B5/4 C6/4 B5/4 G5/4~ G5/12 G5/2 A5/2',
 4: 'B5/4 C6/4 B5/4 G5/4 D5/1 E5/3~ E5/4 C5/8',             # D5 = grace note
 5: 'E5/4 F5/4 E5/4 A4/4 C5/12 C5/2 D5/2',
 6: 'E5/4 F5/4 E5/4 Ab4/4 C5/8 G5/4~ G5/1 D5/1 Db5/1 C5/1',   # sheet: 32nd triplet D-Db-C
 7: 'B4/4 C5/4 B4/4 G4/4~ G4/8 r/2 E4/2 G4/2 A4/2',
 8: 'B4/8 C5/8 Bb4/8 A4/8',
 9: 'r/8 G5/2 F5/2 E5/2 D5/2 E5/2 D5/2 D5/2 C5/2 C5/4 A4/4',
 10: 'r/8 G5/2 F5/2 E5/2 D5/2 E5/2 D5/2 D5/2 C5/2 D5/2 E5/2 G4/4',
 11: 'r/8 G5/2 F5/2 E5/2 D5/2 E5/2 D5/2 D5/2 C5/2 D5/2 E5/2 A4/4',
 12: 'r/6 G4/1 A4/1 G5/2 F5/2 E5/2 D5/2 E5/2 D5/2 D5/2 C5/2 D5/2 E5/2 A4/4',
 13: 'C5/8 G5/2 F5/2 E5/2 D5/2 E5/2 D5/2 D5/2 C5/2 C5/4 Ab4/4',
 14: 'r/6 G4/1 G4/1 G5/2 F5/2 E5/2 D5/2 D5/2 D5/2 G5/2 Ab5/2 G5/8',
 15: 'r/8 B5/2 C6/2 B5/2 G5/2 G5/2 D5/2 G5/2 A5/2 G5/8',
 16: 'r/8 B5/2 C6/2 B5/2 G5/2 G5/2 D5/2 C6/2 D6/2 C6/4 A5/2 G5/2',
 17: 'r/8 A4/2 A4/2 A4/2 C5/2 E5/2 E5/2 D5/2 C5/2 C5/4 A4/4',
 18: 'r/6 G4/1 G4/1 G4/2 G4/2 G4/2 Ab4/2 C5/2 C5/2 C5/2 Ab4/2 G4/4 D4/4',
 19: 'r/8 G4/2 G4/2 G4/2 A4/2 D5/2 D5/2 D5/2 C5/2 C5/4 A4/4',
 20: 'r/6 G4/1 G4/1 G4/2 G4/2 G4/2 A4/2 D5/2 D5/2 D5/2 C5/2 A4/4 E5/4',
 21: 'E5/8 A4/2 A4/2 A4/2 C5/2 E5/2 E5/2 E5/2 D5/2 C5/4 A4/4',
 22: 'r/6 G4/1 G4/1 G5/2 G5/2 G5/2 F5/2 E5/2 D5/2 E5/2 D5/2 C5/2 D5/2 G4/4',
 23: 'r/6 G4/1 G4/1 G4/2 G4/2 G4/2 G4/2 B4/2 B4/2 B4/2 C5/2 D5/6 G4/2',
 24: 'G4/2 A4/2 C5/2 C5/2 C5/2 A4/2 E5/4 E5/8 C5/4 A4/2 G4/2',
 25: 'E5/16 r/8 E5/4 A4/2 G4/2',
 26: 'E5/2 E5/2 F5/2 E5/2 E5/2 E5/2 D5/4 D5/8 B4/4 C5/4',
 27: 'D5/2 D5/2 D5/2 B4/2 A4/4 G4/4 G4/8 B4/4 C5/4',
 28: 'B4/2 G4/2 G4/2 E4/2 G4/2 E4/2 D5/2 E5/2 E5/4 C5/2 C5/2 G5/2 A5/2 G5/4',
 29: 'E5/4 D5/4~ D5/6 C5/2 C5/2 C5/2 A4/2 G4/2 D5/2 E5/2 C5/4',
 30: 'B4/2 A4/2 G4/4~ G4/6 G4/2 G4/2 G4/2 E4/2 D4/2 G4/2 G4/2 G4/2 A4/2',   # sheet: B and A natural here
 31: 'D5/8~ D5/6 G4/2 G4/2 G4/2 E4/2 D4/2 G4/4 A4/4',
 32: 'E5/2 D5/2 E5/12 E5/8 A5/8',
 33: 'C5/2 E4/2 F4/2 C5/2~ C5/2 E4/2 F4/2 C5/2~ C5/2 E4/2 F4/2 C5/2~ C5/2 E4/2 F4/2 C5/2',
 34: 'D5/2 G4/2 Ab4/2 D5/2~ D5/2 G4/2 Ab4/2 G5/2~ G5/2 G4/2 Ab4/2 E5/2~ E5/4 G4/4',
 35: 'B4/2 A4/2 B4/2 E5/2~ E5/2 G4/4 D5/2~ D5/2 G4/2 C5/4 C4/2 B4/6',
 36: 'G4/6 E4/2~ E4/4 C4/4~ C4/6 B3/2 C4/2 D4/2 E4/2 F4/2',
 37: 'G4/16 r/8 C4/4 A3/4',
 38: 'E4/8 Ab3/4 D4/4~ D4/8 C4/4 B3/4',
 39: 'G4/6 D4/2~ D4/4 C4/4~ C4/2 B3/6 C4/4 B3/4',
 40: 'G4/6 C5/2~ C5/4 B4/4~ B4/2 G4/6 A5/4 G5/4',
 41: 'E5/2 D5/2 D5/2 C5/2 C5/2 C5/2 C5/4 A4/8 A5/4 G5/4',
 42: 'E5/2 D5/2 D5/2 C5/2 C5/2 Ab4/2 D5/4 D5/8 Ab5/4 G5/4',
 43: 'E5/2 D5/2 D5/2 D5/2 D5/2 C5/2 D5/2 E5/2 A4/4 G4/4 A5/4 G5/4',
 44: 'E5/2 D5/2 D5/2 C5/2 A4/2 C5/2 E5/2 D5/2 E5/8 A5/4 G5/4',
 45: 'E5/2 D5/2 D5/2 C5/2 C5/2 C5/2 C5/4 A4/4 G4/2 G4/2 A5/4 G5/4',
 46: 'E5/2 D5/2 C5/2 C5/2 C5/2 Ab4/2 C5/2 D5/2 D5/8 C5/2 D5/2 C5/4',
 47: 'B4/2 G4/2 G4/2 G4/2 G4/2 G4/2 G4/2 B4/2 G4/4 E4/4 A4/4 B4/4',
 48: 'C5/4 D5/4 E5/4 F5/4 E5/8 C5/4 A4/2 G4/2',
 49: 'E5/2 D5/2 E5/12 r/8 A5/4 G5/4',
 56: 'B4/2 G4/2 G4/2 G4/2 G4/2 G4/2 G4/2 B4/2 G4/8 D5/4 C5/4',
 57: 'B4/2 G4/2 G4/2 G4/2 G4/2 E4/2 G4/2 A4/2 C5/8 G4/2 B4/2 C5/2 G5/2~',
 58: 'G5/8 E4/8 C5/1 E5/3~ E5/4 E6/8',      # C5 = grace note; E6 -> harmonic string 1 fret 12
}
MEL.update({50: MEL[41], 51: MEL[42], 52: MEL[43], 53: MEL[44], 54: MEL[45], 55: MEL[46]})
HARM = {(58, 24)}                     # (bar, pos): natural harmonic

# ---- piano right hand under the melody (written pitch, shifted with the melody): 'onset32:p1,p2' ----
RH = {
 8: '0:G4,E4 8:G4,E4 16:G4,C#4 24:E4,C#4',
 9: '8:E5,C5 16:C5,A4', 10: '8:C5,Ab4 16:C5,Ab4', 11: '8:E5,B4', 12: '8:D5,B4 16:C#5,G4',
 13: '0:A4,F4,E4 16:C5,A4', 14: '8:C5,Ab4 16:Ab4,F4', 15: '8:G5,E5 16:E5,B4', 16: '8:G5,D5 16:E5,C5',
 17: '8:F4,C4', 18: '8:C4 16:Ab4,F4', 19: '8:D4,B3', 20: '8:D4 16:G4,E4',
 21: '0:C5,A4,F4 16:C5,A4', 22: '8:C5,Ab4 16:B4,G4 24:G4,D4', 23: '8:D4,B3', 24: '0:E4,C4 16:C5,G4',
 25: '0:C5,A4,F4', 26: '0:C5,Ab4 16:Ab4,F4', 27: '0:B4,G4 16:D4', 28: '0:G4,D4 16:C#5,G4',
 29: '0:C5,F4 16:F4', 30: '0:F4,C4 16:C4', 31: '0:B4,G4 16:D4', 32: '0:B4,G4 16:C#5,G4',
 35: '26:G4,D4', 36: '0:E4,C4', 37: '0:F4,E4,C4', 38: '0:C4,Ab3 12:C4,Ab3', 39: '0:D4,C4', 40: '0:E4,C4,B3',
 41: '0:C5,F4 16:F4,C4', 42: '0:C5,Ab4 16:Ab4,F4', 43: '0:B4,G4 24:D5,B4', 44: '0:B4,G4 16:C5,G4',
 45: '0:A4,F#4 16:F#4', 46: '0:C5,Ab4 16:Ab4,F4', 47: '0:G4,D4', 48: '0:G4,E4 16:D5,Bb4,G4 24:G4,E4',
 49: '0:B4,G4', 56: '0:G4,D4', 57: '0:G4,D4 16:G4,E4', 58: '8:C4',
}
RH.update({50: RH[41], 51: RH[42], 52: RH[43], 53: RH[44], 54: '0:C5,A4 16:F4,C4', 55: RH[46]})
def rh(m):
    return [(int(t), A.note_midi(p) + shift(m)) for t, ps in (tok.split(':') for tok in RH.get(m, '').split()) for p in ps.split(',')]

# ---- piano left hand (sounding pitch): 'onset32:pitch', tied continuations omitted ----
# Bars 1-4 are written in the treble clef (D4 A4 F5...): taken one octave lower so the bass sits on the low strings.
LH = {
 1: '0:D3 4:A3 8:F4', 2: '0:F3 4:Ab3 8:C4 12:D4', 3: '0:E3 4:B3 8:D4', 4: '0:A2 4:E3 8:G3 16:A2 16:C3 16:E3 16:G3',
 5: '0:D3 4:A3 8:F4', 6: '0:F3 4:Ab3 8:C4 12:D4', 7: '0:E3 4:B3 8:D4', 8: '0:A2 4:E3 8:G3 16:A2 24:C#3',
 9: '0:D2 4:A2 8:F3 12:D3 16:A3 24:F3', 10: '0:F2 4:C3 8:Ab3 12:F3 16:C4 24:Ab3',
 11: '0:C3 4:G3 8:C4 12:E4 16:C4 24:G3', 12: '0:A2 4:E3 8:B3 12:E3 16:A2 24:E3',
 16: '0:A2 4:E3 8:B3 12:E3 16:A2 24:A3',
 17: '0:D2 4:A2 8:F3 12:D3 16:D2 20:A2 24:F3 28:D3', 18: '0:F2 4:C3 8:Ab3 12:F3 16:F2 20:C3 24:F3 28:F2',
 19: '0:E2 4:B2 8:G3 12:E3 16:E2 20:B2 24:G3 28:E3', 20: '0:A2 4:E3 8:B3 12:E3 16:A2 20:E3 24:C4 28:E3',
 22: '0:G2 4:D3 8:G3 12:D3 16:G2 20:D3 24:F2', 23: '0:E2 4:B2 8:G3 12:B2 16:E2 20:B2 24:G3 28:B2',
 24: '0:A2 4:E3 8:C4 12:E3 16:A2 20:E3 24:C4 28:E3',
 25: '0:D2 4:A2 8:F3 12:D3 16:A3 20:F3 24:D3 28:F3', 26: '0:F2 4:C3 8:Ab3 12:F3 16:C4 20:Ab3 24:F3 28:C3',
 27: '0:E2 4:B2 8:G3 12:E3 16:B3 20:G3 24:E3 28:G3', 28: '0:A2 4:E3 8:B3 12:E3 16:A2 20:E3 24:A3 28:E3',
 30: '0:F2 4:C3 8:Ab3 12:F3 16:Ab3 20:F3 24:C3 28:F3', 32: '0:A2 4:E3 8:G3 16:A2 24:A3',
 33: '0:D3', 34: '0:F3', 35: '0:E3 0:G3 0:D4 30:E3', 36: '0:A2 4:E3 6:A3 18:G3 20:A3', 37: '0:D2 4:A2 8:F3 12:G3',
 38: '0:F2 4:C3 8:F3 12:F2', 39: '0:E2 12:E3', 40: '0:A2 12:A3',
 41: '0:D2 4:A2 8:F3 12:A2 16:D2 20:A2 24:F3 28:A2', 42: '0:F2 4:C3 8:Ab3 12:C3 16:F2 20:C3 24:Ab3 28:C3',
 45: '0:F#2 4:D3 8:A3 12:D3 16:F#2 20:D3 24:A3 28:D3', 48: '0:A2 4:E3 8:C4 12:E3 16:G2 24:C3',
 49: '0:A2 4:E3 8:G3 16:A2 24:A3', 50: '0:D2 4:A2 8:F3 12:A2 16:D3', 51: '0:F2 4:C3 8:Ab3 12:C3 16:F3',
 52: '0:E2 4:B2 8:G3 12:B2 16:E3', 57: '0:A2 4:E3 8:B3 12:E3 16:A2 18:E3 20:B3 22:C4', 58: '0:A2 4:E3 8:A3',
}
LH.update({13: LH[9], 14: LH[10], 15: LH[11], 21: LH[17], 29: LH[25], 31: LH[27], 43: LH[23], 44: LH[20],
           46: LH[42], 47: LH[23], 53: LH[20], 54: LH[50], 55: LH[42], 56: LH[23]})

# ---- chords: bar -> [(pos32, name, degree)]; names as tablib.chord_tones reads them, DISPLAY = how the sheet writes them ----
CH = {
 1: [(0, 'Dm9', 'ii')], 2: [(0, 'Fm6', 'iv')], 3: [(0, 'Em7', 'iii')], 4: [(0, 'Am9', 'vi')],
 5: [(0, 'Dm9', 'ii')], 6: [(0, 'Fm6', 'iv')], 7: [(0, 'Em7', 'iii')],
 8: [(0, 'Am9', 'vi'), (16, 'A7b9', 'V/ii'), (24, 'A/C#', 'V/ii')],
 9: [(0, 'Dm9', 'ii')], 10: [(0, 'Fmmaj7', 'iv')], 11: [(0, 'Cmaj7', 'I')], 12: [(0, 'G/A', 'V'), (16, 'A7', 'V/ii')],
 13: [(0, 'Dm9', 'ii')], 14: [(0, 'Fm6', 'iv')], 15: [(0, 'Cmaj7', 'I')], 16: [(0, 'G/A', 'V'), (16, 'Am7', 'vi')],
 17: [(0, 'Dm9', 'ii')], 18: [(0, 'Fmadd9', 'iv')], 19: [(0, 'Em7', 'iii')], 20: [(0, 'G/A', 'V'), (16, 'Am7add4', 'vi')],
 21: [(0, 'Dm9', 'ii')], 22: [(0, 'Abmaj7/G', 'bVI'), (24, 'Gsus4/F', 'V')], 23: [(0, 'Em7', 'iii')], 24: [(0, 'Am7', 'vi')],
 25: [(0, 'Dm9', 'ii')], 26: [(0, 'Fmmaj7', 'iv'), (16, 'Fm6', 'iv')], 27: [(0, 'Em7', 'iii')], 28: [(0, 'G/A', 'V'), (16, 'A7', 'V/ii')],
 29: [(0, 'Dm9', 'ii')], 30: [(0, 'Fmadd9', 'iv'), (16, 'Fm6', 'iv')], 31: [(0, 'Em7', 'iii')], 32: [(0, 'Em/A', 'iii'), (16, 'A7', 'V/ii')],
 33: [(0, 'Dm9', 'ii')], 34: [(0, 'Fm69', 'iv')], 35: [(0, 'Em7', 'iii')], 36: [(0, 'Am7', 'vi')], 37: [(0, 'Dm11', 'ii')],
 38: [(0, 'Fmmaj7', 'iv'), (12, 'Fm6', 'iv')], 39: [(0, 'Cadd9/E', 'I')], 40: [(0, 'Am9', 'vi')],
 41: [(0, 'Dm9', 'ii')], 42: [(0, 'Fm6', 'iv')], 43: [(0, 'Em7add4', 'iii')], 44: [(0, 'Em7/A', 'iii'), (16, 'Am7', 'vi')],
 45: [(0, 'D7/F#', 'V/V')], 46: [(0, 'Fm6', 'iv')], 47: [(0, 'Em7', 'iii')], 48: [(0, 'Am7', 'vi'), (16, 'Gm7', 'v'), (24, 'C', 'I')],
 49: [(0, 'Em/A', 'iii')], 50: [(0, 'Dm9', 'ii')], 51: [(0, 'Fm6', 'iv')], 52: [(0, 'Em7add4', 'iii')],
 53: [(0, 'Em7/A', 'iii'), (16, 'Am7', 'vi')], 54: [(0, 'Dm9', 'ii')], 55: [(0, 'Fm6', 'iv')], 56: [(0, 'Em7', 'iii')],
 57: [(0, 'G/A', 'V'), (16, 'Am9', 'vi')], 58: [(0, 'Am9', 'vi')],
}
DISPLAY = {'Fmmaj7': 'Fm(maj7)', 'Fmadd9': 'Fm(add9)', 'Fm69': 'Fm6/9', 'Am7add4': 'Am7(add4)', 'Em7add4': 'Em7(add4)',
           'Cadd9/E': 'C(add9)/E', 'A7b9': 'A7b9'}

PLAY = list(range(1, 59))

def parse_mel(m):
    ev, t = [], 0
    for tok in MEL[m].split():
        tie = tok.endswith('~'); tok = tok.rstrip('~')
        n, ln = tok.split('/'); ln = int(ln)
        if n != 'r':
            p = A.note_midi(n) + shift(m); harm = (m, t) in HARM
            s, f = (1, 12) if harm else pos(p)
            ev.append(dict(pos=t, len=ln, s=s, f=f, p=p, tie_out=tie, tied=False, name=n, harm=harm))
        t += ln
    assert t == BAR, (m, t)
    return ev

def melody():
    """melody events per bar, ties marked across bars"""
    bars = [(m, parse_mel(m)) for m in PLAY]
    for i, (m, mel) in enumerate(bars):
        for j, e in enumerate(mel):
            if not e['tie_out']: continue
            nb = bars[i + 1][1] if i + 1 < len(bars) else []
            nxt = mel[j + 1] if j + 1 < len(mel) else (nb[0] if nb and nb[0]['pos'] == 0 else None)
            if nxt and nxt['p'] == e['p']: nxt['tied'] = True
    return dict(bars)

# ---- arrangement ----
DROPPED, OCT = [], []
POS_OVR = {(33, 0, 50): (5, 5)}   # (bar, pos, midi) -> (s, f); D3 off string 4 (melody E-F there)
BASS_END = {}         # (bar, pos) -> the bass stops here
LEGATO = {}

def bars(with_rh=True):
    mel = melody(); out = []
    seq = []
    for i, m in enumerate(PLAY):
        for e in mel[m]:
            e.update(start=i * BAR + e['pos'], end=i * BAR + e['pos'] + e['len'], s0=e['s'], f0=e['f'], lock=False)
            seq.append(e)
    LEGATO.update(A.legato(seq))
    for m in PLAY:
        notes = A.parse_lh(LH.get(m, ''))
        changes = {p for p, _, _ in CH.get(m, [])}
        bass_t = {}
        for t, p in notes:
            low = min(q for t2, q in notes if t2 == t)
            if p == low and (t == 0 or t in changes or p < 48): bass_t[t] = p
        bass = []
        for t, p in sorted(bass_t.items()):
            p = p + 12 if p < 40 else p
            sf = POS_OVR.get((m, t, p)) or min(A.cands(p, (6, 5, 4, 3)), key=lambda sf: (sf[1] > 5, sf[1]))
            bass.append((t, sf, BASS_END[(m, t)]) if (m, t) in BASS_END else (t, sf))
        ev = mel[m]
        extra = rh(m) if with_rh else []
        acc = A.place(m, ev, bass, extra + [(t, p) for t, p in notes if bass_t.get(t) != p], DROPPED, OCT, POS_OVR, span=3, low=4)
        keep = [x for x in acc if not any(b[0] == x[0] and b[1][0] == x[1][0] for b in bass)]   # the bass keeps its string
        DROPPED.extend((m, t, A.pitch(*sf), 'bass string') for t, sf in acc if (t, sf) not in keep)
        bar, d = A.assemble(m, ev, bass, keep); DROPPED.extend(d); out.append(bar)
    return out

def melody_bars():
    mel = melody()
    return [dict(m=m, mel=mel[m], h={}, f=[], b=[], vel=(100, 62, 80, 80)) for m in PLAY]

# ---- page ----
SHOWN = {m: [(p, DISPLAY.get(n, n), d) for p, n, d in v] for m, v in CH.items()}
def chord_at(m, t):
    c = None
    for p, n, d in CH.get(m, []):
        if p <= t: c = n
    return c
SKIP = set(); TAGS = {}
SECTIONS = {1: 'Mở đầu (ô 1–8)', 9: 'Đoạn A (ô 9–16)', 17: 'Đoạn B (ô 17–24)', 25: 'Đoạn C (ô 25–32)',
            33: 'Đoạn chuyển, nhẹ (ô 33–40)', 41: 'Đoạn D (ô 41–48)', 49: 'Kết (ô 49–58)'}
LABEL = {m: ' → '.join(DISPLAY.get(n, n) for _, n, _ in CH[m]) for m in PLAY}
