# Mùa hạ không còn ánh sáng (mhkcas): capo 1, C shapes, tempo 120. Notes: mhkcas.md
# Melody rhythm comes from the user's edited file (mhkcas_melody.tg, written in G shapes at capo 6): every note is +5 here.
# Accompaniment by the bdmt-C principles (fingerstyle-tab-memory.md -> Nguyên lý soạn phần đệm): a written "left hand"
# (open voicing 1-5-9-3 rising then held, rhythm changing per phrase) placed with accomp.place();
# voice 1 = bass only, ringing until the slap on beat 3. Units: 16th notes (16 per bar).
import os, re, zipfile
from tablib import SONGS, PAGES, Q, pitch
import accomp as A

TITLE = 'Mùa hạ không còn ánh sáng'; TG_NAME = 'Mua ha khong con anh sang'
CAPO = 1; TEMPO = 120; STEP = Q // 4; BAR = 16
TG = os.path.join(SONGS, 'mhkcas.tg'); SRC = os.path.join(SONGS, 'mhkcas_melody.tg')
HTML = os.path.join(PAGES, 'mhkcas.html')
STEP8, BAR8 = Q // 2, 8      # the source melody file is read on an eighth-note grid

# melody string/fret in C shapes, one entry per melody note of the bar (in order)
MEL = {
 1: [(1,0)], 2: [(1,0),(1,3),(1,8)], 3: [(1,7),(1,8),(1,7)], 4: [(2,8),(2,5)], 5: [(3,5)],
 6: [(2,1),(1,5),(1,7),(1,8)], 7: [(1,10),(1,7),(1,7)], 8: [(1,5),(1,3)], 9: [(2,1)],
 10: [(1,5),(1,7),(1,8)], 11: [(1,10),(1,8),(1,7)], 12: [(1,9),(1,10),(1,5),(1,3)], 13: [(1,3)],
 14: [(1,5),(1,3),(1,1),(1,0),(1,0),(1,1)], 15: [(1,0),(2,3),(2,1)], 16: [(1,0),(1,0),(1,0),(1,1),(1,0),(2,3)],
 17: [(2,3),(2,1)], 18: [(1,5),(1,4)], 19: [(1,4),(1,4),(1,8),(1,10),(1,8)], 20: [(2,8),(1,7)],
 21: [(1,7),(1,7),(1,7),(1,8),(2,8)], 22: [(1,1),(1,5),(1,7)], 23: [(1,8),(1,10),(1,13),(1,12)], 24: [(1,10)],
}

def melody8():
    xml = zipfile.ZipFile(SRC).read('content.xml').decode('utf8')
    INV = {(8, 0): 1, (4, 0): 2, (4, 1): 3, (2, 0): 4, (2, 1): 6, (1, 0): 8}
    mel = {}
    for mi, mx in enumerate(re.findall(r'<TGMeasure>(.*?)</TGMeasure>', xml, re.S)):
        ev = []
        for b in re.findall(r'<TGBeat>(.*?)</TGBeat>', mx, re.S):
            st = int(re.search(r'<preciseStart>(\d+)', b).group(1))
            v0 = re.search(r'<voice[^>]*>(.*?)</voice>', b, re.S).group(1)
            n = re.search(r'<note([^>]*?)(/>|>(.*?)</note>)', v0, re.S)
            if not n: continue
            d = re.search(r'<duration( dotted="dotted")? value="(\d+)"', v0)
            s = int(re.search(r'string="(\d)"', n.group(1)).group(1)); f = int(re.search(r'value="(\d+)"', n.group(1)).group(1))
            s2, f2 = MEL[mi + 1][len(ev)]
            assert pitch(s2, f2) == pitch(s, f) + 5, ('melody pitch', mi + 1, len(ev))
            ev.append(dict(pos=(st - Q) // STEP8 - mi * BAR8, len=INV[(int(d.group(2)), 1 if d.group(1) else 0)],
                           s=s2, f=f2, hammer='<hammer/>' in (n.group(3) or ''), tied='tiedNote' in n.group(1),
                           slide=(mi + 1, (st - Q) // STEP8 - mi * BAR8) in SLIDES))
        assert len(ev) == len(MEL[mi + 1]), ('melody count', mi + 1)
        mel[mi + 1] = ev
    return mel


VEL = {}  # (melody, harmony/fill, bass, slap) per bar
for m in range(1, 25):
    VEL[m] = (95, 63, 63, 79) if m <= 9 else (95, 79, 79, 79) if m <= 13 else (111, 79, 79, 95) if m <= 17 else (111, 79, 79, 79)

# melody notes that slide into the next melody note on the same string: (bar, pos)
SLIDES = {(7, 0), (23, 2), (23, 5)}   # D->B (10->7), D->F (10->13), E->D into bar 24 (12->10)

# ---- arrangement ----
# bass (pos16, (string, fret)): positions of the earlier arrangement (F bars: F2 on string 6 for the open voicing)
BASS = {
 2: [(0, (5, 3))], 3: [(0, (6, 7))], 4: [(0, (5, 0))], 5: [(0, (5, 0))], 6: [(0, (6, 1))], 7: [(0, (5, 10))],
 8: [(0, (5, 3)), (12, (5, 0))], 9: [(0, (4, 0))], 10: [(0, (6, 3))], 11: [(0, (5, 10))],
 12: [(0, (6, 0)), (12, (5, 0))], 13: [(0, (5, 0))], 14: [(0, (4, 0))], 15: [(0, (4, 0))], 16: [(0, (6, 3))],
 17: [(0, (6, 3)), (12, (4, 2))], 18: [(0, (6, 1))], 19: [(0, (6, 1))], 20: [(0, (6, 0))],
 21: [(0, (5, 0)), (12, (5, 0))], 22: [(0, (4, 0))], 23: [(0, (4, 0))], 24: [(0, (5, 10))],
}
SLAP = 8   # one slap on beat 3, bars 2-24

# the written "left hand" above the bass: 'pos16:pitch' (tab pitch, C shapes)
LH = {
 2: '2:G3 4:D4 6:E4',            # C: 5th, 9th, 3rd, held
 3: '4:G3 6:D4',                 # G/B: light
 4: '2:E3 4:B3 6:C4',            # Am7: 5th, 9th, 3rd
 5: '2:E3 4:G3 6:B3 12:E4',      # Am7, melody rests: keep rising
 6: '2:C3 4:G3 6:A3 12:E4',      # Fmaj7: F2 C3 G3 A3, E = maj7 on top
 7: '2:D4 4:A4',                 # G (barre 10): 5th, 9th
 8: '2:G3 4:D4 6:E4 14:Db4',     # C, then C# leads A7 to Dm7
 9: '2:A3 4:E4 6:F4',            # Dm7, melody rests: D A E F
 10: '2:D3 4:A3 6:B3 12:D4',     # G: G D A B
 11: '2:D4 4:F4',                # G7: 5th, 7th
 12: '2:B2 4:Gb3 6:G3 14:E3',    # Em7: E B F# G, then Am7
 13: '2:E3 4:B3 6:Db4 12:E4',    # A7, melody rests: A E B C#
 14: '2:A3 4:E4 12:C4',          # Dm7: fuller phrase
 15: '2:F3 4:A3 6:C4',           # Dm7
 16: '2:D3 4:A3 6:B3 12:G3',     # G
 17: '2:D3 4:G3 6:B3',           # G, bass E leads to F
 18: '2:C3 4:G3 6:E4 10:Ab3 12:C4',   # Fmaj7 -> Fm (Ab)
 19: '2:C3 4:Ab3 6:C4 12:F4',    # Fm
 20: '2:B2 4:Gb3 6:D4 12:E4',    # Em7: E B F# D
 21: '2:E3 4:G3 6:C4 14:Db4',    # Am7 -> A7 (C#)
 22: '2:A3 4:C4 6:E4',           # Dm7
 23: '2:A3 4:E4 6:F4',           # Dm7 up high
 24: '2:D4 4:A4 6:B4',           # G, wait for the chorus
}

# written "right hand": notes struck with the melody, a 3rd-6th below it (chord tones, held common tones),
# placed before the left hand so they get their strings first
RH = {
 2: '0:G3 6:C4', 3: '0:G4 6:G4', 4: '0:C4 6:C4', 6: '6:E4 12:G4', 7: '0:B4 8:G4', 8: '0:E4 8:Db4',
 9: '12:A3', 10: '0:D4 12:G4', 11: '0:B4 6:F4', 12: '2:B4 6:E4', 13: '14:Db4', 14: '0:F4 6:D4 12:C4',
 15: '2:A3', 16: '0:B3 8:B3', 17: '0:B3', 18: '0:E4 14:F4', 19: '0:F4 8:Ab4', 20: '0:D4 14:G4',
 21: '0:G4 12:Db4', 22: '0:D4 12:F4', 23: '0:A4 10:C5', 24: '0:B4',
}

def lh(m): return [(int(t), A.note_midi(n)) for t, n in (x.split(':') for x in LH.get(m, '').split())]

def melody():
    src = melody8(); out = {}
    for m in range(1, 25):
        out[m] = [dict(e, pos=e['pos'] * 2, len=e['len'] * 2, p=pitch(e['s'], e['f']), tie_out=False) for e in src[m]]
    for m in range(1, 25):                      # tie_out = the next note continues this one
        nxt = out.get(m + 1, [])
        for j, e in enumerate(out[m]):
            n2 = out[m][j + 1] if j + 1 < len(out[m]) else (nxt[0] if nxt and nxt[0]['pos'] == 0 else None)
            e['tie_out'] = bool(n2 and n2['tied'])
    return out

DROPPED = []

def bars():
    mel = melody(); out = []
    for m in range(1, 25):
        bass = BASS.get(m, [])
        acc = A.place(m, mel[m], bass, A.parse_lh(RH.get(m, '')) + lh(m), DROPPED)
        bar, d = A.assemble(m, mel[m], bass, acc, slaps=(SLAP,) if m >= 2 else (), vel=VEL[m])
        DROPPED.extend(d); out.append(bar)
    return out

# ---- page ----
CHORDS = {  # bar -> [(pos, name, root, degree)]
 2:[(0,'C','C','I')], 3:[(0,'G/B','G','V')], 4:[(0,'Am7','A','vi')], 5:[(0,'Am7','A','vi')],
 6:[(0,'Fmaj7','F','IV')], 7:[(0,'G','G','V')], 8:[(0,'C','C','I'),(4,'A7','A','V/ii')], 9:[(0,'Dm7','D','ii')],
 10:[(0,'G','G','V')], 11:[(0,'G7','G','V')], 12:[(0,'Em7','E','iii'),(4,'Am7','A','vi')], 13:[(0,'A7','A','V/ii')],
 14:[(0,'Dm7','D','ii')], 15:[(0,'Dm7','D','ii')], 16:[(0,'G','G','V')], 17:[(0,'G','G','V')],
 18:[(0,'Fmaj7','F','IV'),(4,'Fm','F','iv')], 19:[(0,'Fm','F','iv')], 20:[(0,'Em7','E','iii')],
 21:[(0,'Am7','A','vi'),(6,'A7','A','V/ii')], 22:[(0,'Dm7','D','ii')], 23:[(0,'Dm7','D','ii')], 24:[(0,'G','G','V')],
}
SHOWN = {m: [(p * 2, n, d) for p, n, r, d in v] for m, v in CHORDS.items()}   # CHORDS positions are eighths
def chord_at8(m, t):
    c = None
    for p, n, r, d in CHORDS.get(m, []):
        if p <= t: c = n
    return c
def chord_at(m, t): return chord_at8(m, t // 2)
LABEL = {
 1: 'lấy đà, chưa có hợp âm',
 2: 'C: G tay phải dưới E, rải G–D, C dưới G', 3: 'G/B: bass B (hợp âm đảo), G tay phải ngân', 4: 'Am7: C tay phải giữ dưới giai điệu, rải E–B',
 5: 'giai điệu nghỉ: rải Am7 đi lên tới E', 6: 'Fmaj7: bass F dây 6, E tay phải là maj7', 7: 'G: chặn phím 10, B rồi G tay phải',
 8: 'C rồi A7: C# tay phải dẫn về Dm7', 9: 'giai điệu nghỉ: rải Dm7 D–A–E–F, A dưới C',
 10: 'G: D tay phải dưới A, rải G–D–A–B', 11: 'G7: B–F tay phải (quãng 3 cung)', 12: 'Em7 rồi Am7: B, E tay phải',
 13: 'giai điệu nghỉ: rải A7, C# dưới G cuối ô', 14: 'Dm7: câu 3 dày hơn, F–D–C tay phải đi xuống', 15: 'Dm7: A tay phải dưới D ngân, rải F–A–C',
 16: 'G: B tay phải lặp ở phách 1 & 3', 17: 'G: bass E cuối ô dẫn sang F', 18: 'Fmaj7 rồi Fm: E tay phải là maj7, Ab ở phách 3',
 19: 'Fm: rải F–C–Ab–C dưới giai điệu cao', 20: 'Em7: D (7th) tay phải, G dưới B cuối ô', 21: 'Am7 rồi A7: G tay phải, C# cuối ô',
 22: 'Dm7: D, F tay phải dưới giai điệu', 23: 'lên phím 13: A tay phải, rải A–E–F', 24: 'dừng ở G (bậc V), B tay phải, chờ cao trào',
}
SECTIONS = {1:'Lấy đà', 2:'Câu 1 (ô 2–9)', 10:'Câu 2 (ô 10–13)', 14:'Câu 3 (ô 14–17)', 18:'Dẫn vào cao trào (ô 18–24)'}
SKIP = set(); TAGS = {}
