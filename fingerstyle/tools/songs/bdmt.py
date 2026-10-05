# Bèo dạt mây trôi (bdmt): no capo, C shapes, tempo 120. Notes: bdmt.md
# Melody = top line of the piano sheet (Desktop\Bèo dạt mây trôi.pdf, Vu Ngoc Tien), one octave below written pitch,
# re-fingered for h/p/s pairs (accomp.legato). Chords read from the piano left hand.
# Accompaniment = the piano left hand note for note (LH), placed with accomp.place(): each note keeps its pitch and
# onset (below E2: one octave up; at/above the melody: one octave down; same as the ringing bass: dropped).
# Bass = the left-hand note on beat 1, on a chord change, or below C3 on the sheet; voice 1 = bass only, ringing.
# Units: 16th notes (16 per bar). Bars keyed by sheet number; sheet bar 1 is empty, playing starts at bar 2.
import os
from tablib import SONGS, PAGES, Q, pitch
import accomp as A

TITLE = 'Bèo dạt mây trôi'; TG_NAME = 'Beo dat may troi'
CAPO = 0; TEMPO = 120; STEP = Q // 4; BAR = 16
TG = os.path.join(SONGS, 'bdmt.tg'); MELODY_TG = os.path.join(SONGS, 'bdmt_melody.tg')
HTML = os.path.join(PAGES, 'bdmt.html')

NAMES = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
def midi(n):  # 'Eb5' -> written midi, sounding = -12
    acc = -1 if n[1:2] == 'b' else 0
    return 12 * (int(n[-1]) + 1) + NAMES[n[0]] + acc - 12
POS = {43: (6, 3), 48: (5, 3), 50: (4, 0), 52: (4, 2), 53: (4, 3), 55: (3, 0), 57: (3, 2), 58: (3, 3),
       59: (2, 0), 60: (2, 1), 62: (2, 3), 63: (2, 4), 64: (1, 0), 65: (1, 1), 67: (1, 3), 69: (1, 5),
       72: (1, 8), 79: (3, 5)}   # G5 = natural harmonic, string 3 fret 5 (fret 15 sounded harsh)

# ---- melody, written pitch: NOTE/len16, '~' = tied into next note, r/len = rest ----
MEL = {
 2: 'r/8 C5/8',
 3: 'C5/8 G5/2 F5/2 E5/2 F5/2',            4: 'G5/8 G5/1 A5/1~ A5/2 G5/4',
 5: 'G5/8 D5/1 E5/1~ E5/2~ E5/4',          6: 'E5/6 D5/2 E5/2 D5/2 E5/2 G5/2',
 7: 'C5/6 G4/1 A4/1 C5/2 E5/2 D5/2 C5/2',  8: 'G4/2 A4/2 G4/3 D4/1 G4/1 C5/1 G5/1 C6/1 G6/4',
 9: 'G5/4 F5/2 G5/1 F5/1 E5/4 F5/4',       10: 'G5/6~ G5/1 G4/1 D5/1 E5/1~ E5/2~ E5/4',
 11: 'E5/8 E5/2 D5/2 E5/2 G5/2',           12: 'C5/8 C5/2 E5/2 D5/2 C5/2',
 13: 'G4/8 D4/8',                          14: 'C5/1 A4/1~ A4/2 C5/4 C5/4 D5/2 E5/2',
 15: 'E5/8~ E5/2 G4/2 C5/2 D5/2',          16: 'E5/6 D5/2 E5/4 D5/2 Eb5/1 D5/1',
 17: 'C5/6 D5/2 E5/2 D5/2 E5/2 G5/2',      18: 'C5/4 G4/8 C5/4',
 19: 'G4/4 C5/4 E5/4 D5/2 E5/1 D5/1',      20: 'C5/8 F4/4 C4/2 F4/2',
 21: 'G4/1 E4/1~ E4/2~ E4/4 C5/2 E4/2 G4/4',
 22: 'C5/8 G5/2 F5/2 E5/2 F5/2',           23: 'G5/6~ G5/1 C5/1 G5/1 A5/1~ A5/2 G5/4',
 24: 'G5/8 D5/1 E5/1~ E5/2~ E5/4',         25: 'E5/6 D5/2 E5/2 D5/2 E5/2 G5/2',
 26: 'C5/8 C5/2 E5/2 D5/2 C5/2',           27: 'G4/16',
 28: 'G5/6 C6/2~ C6/2 E5/1 F5/1 E5/2 F5/2', 29: 'G5/8 E5/4 G4/2 C5/1 D5/1',
 30: 'E5/6 D5/2 E5/2 D5/2 E5/2 G5/2',      31: 'C5/4 G4/12',
 32: 'C5/8 E5/4 D5/4',                     33: 'C5/8 F4/4 C4/2 F4/2',
 34: 'D4/1 E4/1~ E4/2~ E4/4 C5/4 E4/2 G4/2',
 35: 'C5/8 G5/2 F5/2 E5/2 F5/2',           36: 'G5/4 G4/4~ G4/2 E5/2~ E5/2 D5/2',
 37: 'E5/8 E5/2 D5/2 E5/2 G5/2',           38: 'C5/8 C5/2 E5/2 D5/2 C5/2',
 39: 'G4/8 G4/6~ G4/1 Bb4/1',              40: 'A4/4 C5/4 C5/3 D5/1~ D5/2 E5/2',
 41: 'E5/8 E5/4 G4/2 D5/2',                42: 'E5/6 D5/2 E5/4 D5/2 Eb5/1 D5/1',
 43: 'C5/6 D5/2 E5/2 D5/2 E5/2 G5/2',      44: 'C5/4 G4/8 C5/2 A4/1 C5/1',
 45: 'G4/4 C5/4 E5/4 D5/4',                46: 'C5/8 F4/4 C4/2 F4/2',
 47: 'D4/1 E4/1~ E4/2~ E4/4 G4/8',         48: 'C5/1 A4/1~ A4/2 C5/4 C5/4 D5/2 E5/2',
 49: 'E5/8 C5/4 D5/4',                     50: 'E5/6 D5/2 E5/4 D5/2 Eb5/1 D5/1',
 51: 'C5/6 D5/2 E5/2 D5/2 E5/2 G5/2',      52: 'C5/4 G4/4 E4/4 C5/4',
 53: 'G4/4 C5/4 E5/4 D5/2 E5/1 D5/1',      54: 'C5/12 G5/2 C6/2',
 55: 'G6/8 C5/2 G4/2 C5/2 G5/2~',          56: 'G5/8 C5/2 D5/2 C5/2 G5/2~',
 57: 'G5/8~ G5/2 G4/2 C5/2 D5/2',          58: 'F5/4 E5/4 C5/4 G4/4',
 59: 'C5/8 G4/8',                          60: 'E4/4 G3/1 C4/1 F4/1 G4/1 C5/2 C5/1 F5/1 G4/1 C5/1 F5/1 G5/1',
 61: 'C6/16',   # sheet: 8va (C7); played without the 8va, fret 8
}

# ---- chords: bar -> [(pos16, name, degree)] ----
CH = {
 2: [(0, 'C', 'I')], 3: [(0, 'C', 'I')], 4: [(0, 'G', 'V')], 5: [(0, 'Am', 'vi')],
 6: [(0, 'Gm7', 'ii/IV'), (8, 'C7', 'V/IV')], 7: [(0, 'F', 'IV')], 8: [(0, 'G', 'V')], 9: [(0, 'C', 'I')],
 10: [(0, 'Em', 'iii'), (12, 'E7/G#', 'V/vi')], 11: [(0, 'Am', 'vi')], 12: [(0, 'F', 'IV')],
 13: [(0, 'G', 'V'), (8, 'Gsus4', 'V')], 14: [(0, 'F', 'IV')], 15: [(0, 'C', 'I')],
 16: [(0, 'Em7', 'iii'), (8, 'Ab', 'bVI')], 17: [(0, 'Am7', 'vi')], 18: [(0, 'F', 'IV')], 19: [(0, 'G', 'V')],
 20: [(0, 'C', 'I')], 21: [(0, 'C', 'I')],
 22: [(0, 'C', 'I')], 23: [(0, 'G', 'V')], 24: [(0, 'Am', 'vi')], 25: [(0, 'Gm7', 'ii/IV'), (8, 'C7', 'V/IV')],
 26: [(0, 'F', 'IV')], 27: [(0, 'G', 'V')],
 28: [(0, 'C', 'I')], 29: [(0, 'G', 'V')], 30: [(0, 'Am', 'vi'), (8, 'C7/G', 'V/IV')], 31: [(0, 'F', 'IV')],
 32: [(0, 'G', 'V')], 33: [(0, 'C', 'I')], 34: [(0, 'C', 'I')],
 35: [(0, 'C', 'I')], 36: [(0, 'Em', 'iii'), (12, 'E7/G#', 'V/vi')], 37: [(0, 'Am', 'vi')], 38: [(0, 'F', 'IV')],
 39: [(0, 'G', 'V')], 40: [(0, 'F', 'IV')], 41: [(0, 'C', 'I')],
 42: [(0, 'Bm7b5', 'ii/vi'), (8, 'E7', 'V/vi'), (12, 'Ab', 'bVI')], 43: [(0, 'Am7', 'vi')], 44: [(0, 'F', 'IV')],
 45: [(0, 'G', 'V')], 46: [(0, 'C', 'I')], 47: [(0, 'C', 'I')], 48: [(0, 'F', 'IV')],
 49: [(0, 'C/E', 'I')], 50: [(0, 'Bm7b5', 'ii/vi'), (8, 'E7', 'V/vi')], 51: [(0, 'Am7', 'vi')],
 52: [(0, 'Dm7', 'ii'), (8, 'C/E', 'I')], 53: [(0, 'F', 'IV'), (8, 'G', 'V')],
 54: [(0, 'F', 'IV')], 55: [(0, 'F/A', 'IV')], 56: [(0, 'C/E', 'I')], 57: [(0, 'C/E', 'I')], 58: [(0, 'Dm', 'ii')],
 59: [(0, 'Gsus4', 'V')], 60: [(0, 'C', 'I')], 61: [(0, 'C', 'I')],
}

H = {13: {8: [(5, 3)]}, 59: {8: [(5, 3), (4, 0)]}, 61: {0: [(3, 5), (2, 5)]}}

PLAY = list(range(2, 62))

def parse_mel(m):
    ev, t = [], 0
    for tok in MEL[m].split():
        tie = tok.endswith('~'); tok = tok.rstrip('~')
        n, ln = tok.split('/'); ln = int(ln)
        if n != 'r':
            s, f = POS[midi(n)]
            ev.append(dict(pos=t, len=ln, s=s, f=f, p=midi(n), tie_out=tie, tied=False, name=n, harm=midi(n) == 79))
        t += ln
    assert t == 16, (m, t)
    return ev

def melody():
    """melody events per bar, ties marked across bars"""
    bars = [(m, parse_mel(m)) for m in PLAY]
    for i, (m, mel) in enumerate(bars):   # ties: continuation = next melody note (or first note of the next bar), same pitch
        for j, e in enumerate(mel):
            if not e['tie_out']: continue
            nb = bars[i + 1][1] if i + 1 < len(bars) else []
            nxt = mel[j + 1] if j + 1 < len(mel) else (nb[0] if nb and nb[0]['pos'] == 0 else None)
            if nxt and nxt['p'] == e['p']: nxt['tied'] = True
    return dict(bars)

# ---- piano left hand, read from the sheet: 'onset16:pitch', tied continuations omitted ----
LH = {
 3: '0:C3 4:G3 8:D4', 4: '0:G2 2:G3 4:B3 6:D4 8:G4', 5: '0:A2 2:E3 4:A3 6:B3 8:C4',
 6: '0:G2 2:D3 4:Bb3 8:C3 10:G3 12:D4', 7: '0:F3 2:C4 4:F3 4:F4', 8: '0:G2 2:D3 4:A3 6:B3',
 9: '0:C3 2:G3 4:D4 8:E4', 10: '0:E2 2:B2 4:E3 6:G3 8:B3 12:Ab2', 11: '0:A2 2:E3 4:A3 6:C4 8:E4',
 12: '0:F2 2:C3 4:G3 6:A3 8:C4', 13: '0:G2 4:D3', 14: '0:F2 2:C3 4:G3 6:A3 8:C4 10:F4',
 15: '0:C3 2:G3 4:D4 6:G3 8:E4', 16: '0:E3 2:B3 4:D4 8:Ab2 8:Ab3', 17: '0:A2 2:E3 4:A3 6:C4 8:E4 8:G4',
 18: '0:F2 2:C3 4:F3 6:G3 8:A3', 19: '0:G2 2:D3 4:G3 6:A3 8:B3', 20: '0:C3 2:G3 4:C4 6:D4 10:G3',
 21: '0:C3 8:G3 10:D4', 22: '0:C2 2:G2 4:D3 6:E3 8:G3 10:C4', 23: '0:G2 2:G3 4:B3 6:D4 8:G4',
 24: '0:A2 2:E3 4:A3 6:B3 8:C4', 25: '0:G2 2:D3 4:Bb3 8:C3 10:G3 12:E4', 26: '0:F2 2:C3 4:G3 6:A3',
 27: '0:G2 2:D3 4:A3 6:D3 8:B3 12:D3', 28: '0:C2 2:G2 4:D3 6:E3 8:G3', 29: '0:G1 2:G2 4:D3 6:G3 10:Ab2',
 30: '0:A2 2:E3 4:A3 8:G2 12:C3 12:G3', 31: '0:F2 2:C3 4:G3 6:A3 8:C4', 32: '0:G2 2:D3 4:G3 6:B3 8:D4',
 33: '0:C2 4:C3 6:G3 10:G3', 34: '0:C3 6:G3 8:D4 12:G3', 35: '0:C2 4:C3 6:G3 8:C4 14:D2',
 36: '0:E2 0:E3 8:B3 8:E4 12:Ab2', 37: '0:A2 2:E3 4:A3 6:C4 8:E4', 38: '0:F2 2:C3 4:G3 6:A3 8:C4',
 39: '0:G2 2:D3 4:A3 6:G2 8:B3 10:G3 12:D3', 40: '0:F2 2:C3 4:G3 6:A3 8:C4 10:A3',
 41: '0:C2 2:G2 4:D3 6:E3 8:G3 10:C4', 42: '0:B2 2:F3 4:A3 8:E2 8:E3 12:Ab2 12:Ab3',
 43: '0:A2 2:E3 4:A3 6:C4', 44: '0:F2 2:C3 4:G3 6:A3 8:C4', 45: '0:G2 2:D3 4:A3 6:B3 8:D4',
 46: '0:C2 4:C3 6:G3 10:G3', 47: '0:C3 4:G3 10:C4', 48: '0:F2 2:C3 4:G3 6:A3 10:C4',
 49: '0:E3 2:C4 4:E4 6:G4', 50: '0:B2 2:F3 4:A3 8:E3 8:B3', 51: '0:A3 2:E4 4:A4', 52: '0:D3 2:C4 8:E3 8:C4',
 53: '0:F3 2:C4 8:G2 8:G3', 54: '0:F2 2:C3 4:G3 6:A3 8:C4 10:G4', 56: '0:E3 2:C4 4:E4 6:G4',
 58: '0:D3 2:A3 6:D4 10:A3', 59: '0:G2 4:D3 8:A3', 60: '0:C2 2:C3', 61: '0:C3',
}

# ---- arrangement ----
DROPPED, OCT = [], []
# fixes for stretches: a fretted bass ringing under a high melody
POS_OVR = {(61, 0, 48): (6, 8)}   # (bar, pos, midi) -> (s, f)
BASS_END = {(8, 0): 10, (28, 2): 6, (54, 0): 14}       # (bar, pos) -> the bass stops here

LEGATO = {}   # counts of h/p and slides from accomp.legato()

def bars():
    mel = melody(); out = []
    seq = []
    for i, m in enumerate(PLAY):          # melody re-fingered for as many h/p/s as possible
        for e in mel[m]:
            e.update(start=i * 16 + e['pos'], end=i * 16 + e['pos'] + e['len'], s0=e['s'], f0=e['f'],
                     lock=e['pos'] in H.get(m, {}))   # fixed harmony under it: keep the position
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
        acc = A.place(m, ev, bass, [(t, p) for t, p in notes if bass_t.get(t) != p], DROPPED, OCT, POS_OVR)
        bar, d = A.assemble(m, ev, bass, acc, h0=H.get(m)); DROPPED.extend(d); out.append(bar)
    return out

def melody_bars():
    mel = melody()
    return [dict(m=m, mel=mel[m], h={}, f=[], b=[], vel=(100, 62, 80, 80)) for m in PLAY]

# ---- page ----
SHOWN = {m: [(p, n, d) for p, n, d in v] for m, v in CH.items()}
def chord_at(m, t):
    c = None
    for p, n, d in CH.get(m, []):
        if p <= t: c = n
    return c
SKIP = set(); TAGS = {}
SECTIONS = {2: 'Lấy đà', 3: 'Câu 1 (ô 3–9)', 10: 'Câu 2 (ô 10–15)', 16: 'Câu 3 (ô 16–21)', 22: 'Câu 1 lặp lại (ô 22–27)',
            28: 'Câu 4 (ô 28–34)', 35: 'Câu 5 (ô 35–41)', 42: 'Câu 6 (ô 42–48)', 49: 'Câu 7 (ô 49–53)', 54: 'Kết (ô 54–61)'}

LABEL = {
 2: 'lấy đà: nốt C, chưa có đệm', 3: 'C: rải C–G–D (9th) đi lên rồi ngân', 4: 'G: rải lên tới G cao, bass ngân',
 5: 'Am: B (9th) trên đỉnh phần rải', 6: 'Gm7 → C7: dẫn về F (ii–V của IV)', 7: 'F: bass F ngân, C chen dưới bass',
 8: 'câu chạy lên G cao: harmonic dây 3 phím 5', 9: 'C: rải C–G–D–E dưới giai điệu móc kép',
 10: 'Em rồi E7/G#: bass G# dẫn về Am', 11: 'Am: rải lên tới E', 12: 'F: rải F–C–G–A (9th)',
 13: 'G rồi Gsus4: cụm A–C–D', 14: 'F: rải lên tới F cao', 15: 'C: bass ngân, rải G–D–G–E',
 16: 'Em7 rồi Ab (hợp âm mượn), Eb trong giai điệu', 17: 'Am7: G trên đỉnh phần rải là 7th',
 18: 'F: rải F–C–F–G–A', 19: 'G: rải G–D–G–A–B đi lên', 20: 'C: giai điệu xuống thấp, đệm thưa',
 21: 'C: giai điệu ngân E thấp, G và D chen vào', 22: 'lặp lại câu đầu: C rải C–G–D–E',
 23: 'G: rải tới G cao, giai điệu lên A', 24: 'Am: B (9th) trên đỉnh, giai điệu ngân E',
 25: 'Gm7 → C7: E ở đỉnh C7', 26: 'F: rải F–C–G–A dưới nốt C ngân', 27: 'G: giai điệu ngân G cả ô, đệm chạy G–D–A–D–B',
 28: 'C: giai điệu lên C cao (phím 8), bass cắt sớm', 29: 'G: bass đi G → G# → A', 30: 'Am rồi C7/G: bass G dẫn về F',
 31: 'F: giai điệu ngân G, đệm rải phía dưới', 32: 'G: rải lên tới D', 33: 'C: bass C ngân, G lặp lại',
 34: 'C: giai điệu E thấp, D chen vào', 35: 'C: bass D cuối ô dẫn lên E', 36: 'Em rồi E7/G# ở phách 4',
 37: 'Am: rải A–E–A–C–E', 38: 'F: rải lên tới C', 39: 'G: giai điệu ngân G, đệm G–D–A–G–B–G–D',
 40: 'F: rải F–C–G–A–C–A', 41: 'C: rải C–G–D–E–G–C', 42: 'Bm7b5 → E7 → Ab: dẫn về Am',
 43: 'Am7: rải A–E–A–C', 44: 'F: giai điệu ngân G, đệm F–C–G–A', 45: 'G: rải G–D–A–B–D',
 46: 'C: giai điệu xuống C thấp, bass ngân', 47: 'C: giai điệu ngân G, C cuối ô', 48: 'F: giai điệu móc kép, rải F–C–G–A',
 49: 'C/E: bass E (3rd)', 50: 'Bm7b5 → E7 dẫn về Am', 51: 'Am: bass A cao, rải A–E–A',
 52: 'Dm7 → C/E: bass đi D → E', 53: 'F → G: bass đi tiếp F → G', 54: 'F: chuẩn bị lên cao, bass dừng trước C cao',
 55: 'G cao harmonic, đệm nghỉ', 56: 'C/E: bass E, rải C–E–G', 57: 'C/E: G ngân sang ô sau', 58: 'Dm: bass D, rải A–D–A',
 59: 'Gsus4: cụm C–D dưới G', 60: 'C: câu chạy kết, bass C', 61: 'kết: chặn C (phím 8, 5, 5, 8)',
}
