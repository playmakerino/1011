# Mùa hạ không còn ánh sáng (mhkcas): hand-written arrangement, capo 1, C shapes (same pitch as the old capo 6 / G-shape version).
# Melody rhythm comes from the user's edited file (mhkcas_melody.tg, written in G shapes at capo 6): every note is +5 here.
# voice 0 = melody (+ harmony notes struck with it) + fills in melody rests; voice 1 = bass (sustained) + slaps.
# Units: eighth notes (8 per bar). Notes: mhkcas.md
import os, re, zipfile
from tablib import SONGS, PAGES, Q, X, pitch

TITLE = 'Mùa hạ không còn ánh sáng'; TG_NAME = 'Mua ha khong con anh sang'
CAPO = 1; TEMPO = 120; STEP = Q // 2; BAR = 8
TG = os.path.join(SONGS, 'mhkcas.tg'); SRC = os.path.join(SONGS, 'mhkcas_melody.tg')
HTML = os.path.join(PAGES, 'mhkcas.html')

# melody string/fret in C shapes, one entry per melody note of the bar (in order)
MEL = {
 1: [(1,0)], 2: [(1,0),(1,3),(1,8)], 3: [(1,7),(1,8),(1,7)], 4: [(2,8),(2,5)], 5: [(3,5)],
 6: [(2,1),(1,5),(1,7),(1,8)], 7: [(1,10),(1,7),(1,7)], 8: [(1,5),(1,3)], 9: [(2,1)],
 10: [(1,5),(1,7),(1,8)], 11: [(1,10),(1,8),(1,7)], 12: [(1,9),(1,10),(1,5),(1,3)], 13: [(1,3)],
 14: [(1,5),(1,3),(1,1),(1,0),(1,0),(1,1)], 15: [(1,0),(2,3),(2,1)], 16: [(1,0),(1,0),(1,0),(1,1),(1,0),(2,3)],
 17: [(2,3),(2,1)], 18: [(1,5),(1,4)], 19: [(1,4),(1,4),(1,8),(1,10),(1,8)], 20: [(2,8),(1,7)],
 21: [(1,7),(1,7),(1,7),(1,8),(2,8)], 22: [(1,1),(1,5),(1,7)], 23: [(1,8),(1,10),(1,13),(1,12)], 24: [(1,10)],
}

def melody():
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
            ev.append(dict(pos=(st - Q) // STEP - mi * BAR, len=INV[(int(d.group(2)), 1 if d.group(1) else 0)],
                           s=s2, f=f2, hammer='<hammer/>' in (n.group(3) or ''), tied='tiedNote' in n.group(1),
                           slide=(mi + 1, (st - Q) // STEP - mi * BAR) in SLIDES))
        assert len(ev) == len(MEL[mi + 1]), ('melody count', mi + 1)
        mel[mi + 1] = ev
    return mel

# h: harmony notes added to the melody note starting at pos
# f: fills (pos, len, notes) inside melody rests (voice 0)
# b: voice 1 (pos, len, notes)
A = {
 # --- Verse: very sparse, bass rings the whole bar ---
 1:  dict(h={}, f=[], b=[]),
 2:  dict(h={0:[(2,1)]}, f=[], b=[(0,4,[(5,3)]),(4,4,[(5,X)])]),                                   # C
 3:  dict(h={0:[(2,8)], 3:[(3,7)]}, f=[(7,1,[(2,8)])], b=[(0,4,[(6,7)]),(4,4,[(6,X)])]),            # G/B, 7th position
 4:  dict(h={0:[(3,5)], 3:[(4,7)]}, f=[(7,1,[(3,5)])], b=[(0,4,[(5,0)]),(4,4,[(5,X)])]),            # Am7
 5:  dict(h={}, f=[(1,1,[(4,7)]),(2,1,[(3,5)]),(3,2,[(2,8)]),(5,2,[(2,5)])],          # Am7: echo G->E of bar 4
          b=[(0,4,[(5,0)]),(4,4,[(5,X)])]),
 6:  dict(h={0:[(3,2)], 3:[(2,5)]}, f=[], b=[(0,4,[(4,3)]),(4,4,[(6,X)])]),                         # Fmaj7
 7:  dict(h={0:[(3,12),(4,12)], 4:[(2,8)]}, f=[], b=[(0,4,[(5,10)]),(4,4,[(6,X)])]),                # G, barre 10
 8:  dict(h={0:[(2,5),(3,5)]}, f=[(6,1,[(2,2)]),(7,1,[(3,2)])],                       # C -> A7 (C# leads to Dm)
          b=[(0,4,[(5,3)]),(4,2,[(5,X)]),(6,2,[(5, 0)])]),
 9:  dict(h={}, f=[(1,1,[(3,2)]),(2,1,[(2,3)]),(3,3,[(1,1)])], b=[(0,4,[(4,0)]),(4,4,[(6,X)])]),     # Dm7
 # --- a little more motion ---
 10: dict(h={0:[(2,3),(3,0)]}, f=[(4,1,[(3,7)]),(5,1,[(2,8)])], b=[(0,4,[(6,3)]),(4,4,[(6,X)])]),   # G (add9)
 11: dict(h={0:[(2,12),(3,10)], 3:[(3,10)]}, f=[(7,1,[(3,7)])], b=[(0,4,[(5,10)]),(4,4,[(6,X)])]),  # G7 (F-B tritone)
 12: dict(h={1:[(3,9)], 3:[(2,3)]}, f=[(7,1,[(2,1)])],                                # Em7 -> Am7
          b=[(0,4,[(6,0)]),(4,2,[(6,X)]),(6,2,[(5, 0)])]),
 13: dict(h={}, f=[(1,1,[(3,2)]),(2,1,[(2,2)]),(3,1,[(1,0)]),(4,2,[(3,0)])],          # A7
          b=[(0,4,[(5,0)]),(4,4,[(5,X)])]),
 # --- second phrase: fuller ---
 14: dict(h={0:[(2,3),(3,2)], 3:[(2,1)]}, f=[], b=[(0,4,[(4,0)]),(4,4,[(6,X)])]),     # Dm7
 15: dict(h={0:[(3,2)]}, f=[(5,1,[(1,1)]),(6,1,[(1,0)])], b=[(0,4,[(4,0)]),(4,4,[(6,X)])]),  # Dm7, fill F-E
 16: dict(h={0:[(2,3)]}, f=[], b=[(0,4,[(6,3)]),(4,4,[(6,X)])]),         # G6
 17: dict(h={}, f=[(2,1,[(1,3)]),(3,1,[(1,0)]),(4,2,[(2,3)])],                        # G: falling line G-E-D into melody C
          b=[(0,4,[(6,3)]),(4,2,[(6,X)]),(6,2,[(4, 2)])]),                                                # bass G then E -> F of bar 18
 # --- pre-chorus ---
 18: dict(h={0:[(2,5),(3,5)]}, f=[(4,1,[(3,1)]),(5,1,[(2,1)]),(6,1,[(1,1)])],         # Fmaj7 -> Fm (Ab in the fill)
          b=[(0,4,[(4,3)]),(4,4,[(6,X)])]),
 19: dict(h={0:[(2,6)], 2:[(3,5)], 6:[(2,9)]}, f=[],                                  # Fm (D = 6th)
          b=[(0,4,[(4,3)]),(4,4,[(6,X)])]),
 20: dict(h={0:[(3,7)]}, f=[(4,1,[(4,9)]),(5,1,[(3,7)]),(6,1,[(2,8)])],               # Em7
          b=[(0,4,[(6,0)]),(4,4,[(6,X)])]),
 21: dict(h={0:[(2,5),(3,5)], 2:[(3,5)], 6:[(3,6)]}, f=[],                            # Am7 -> A7 (C# on beat 4)
          b=[(0,4,[(5,0)]),(4,2,[(5,X)]),(6,2,[(5,0)])]),
 22: dict(h={0:[(2,3),(3,2)]}, f=[(4,1,[(2,1)]),(5,1,[(1,1)])],                       # Dm7
          b=[(0,4,[(4,0)]),(4,4,[(6,X)])]),
 23: dict(h={0:[(2,6),(3,7)], 2:[(2,10)], 3:[(2,10)], 5:[(2,10)]}, f=[],              # Dm7 up high, open D bass
          b=[(0,4,[(4,0)]),(4,4,[(6,X)])]),
 24: dict(h={0:[(3,12),(4,12)]}, f=[(4,1,[(3,7)]),(5,1,[(2,8)]),(6,2,[(1,7)])],       # G barre 10, rising fill D-G-B
          b=[(0,4,[(5,10)]),(4,4,[(6,X)])]),
}

VEL = {}  # (melody, harmony/fill, bass, slap) per bar
for m in range(1, 25):
    VEL[m] = (95, 63, 63, 79) if m <= 9 else (95, 79, 79, 79) if m <= 13 else (111, 79, 79, 95) if m <= 17 else (111, 79, 79, 79)

# melody notes that slide into the next melody note on the same string: (bar, pos)
SLIDES = {(7, 0), (23, 2), (23, 5)}   # D->B (10->7), D->F (10->13), E->D into bar 24 (12->10)

def bars():
    mel = melody()
    return [dict(m=m, mel=mel[m], h=A[m]['h'], f=A[m]['f'], b=[(p, ln, list(ns)) for p, ln, ns in A[m]['b']], vel=VEL[m])
            for m in range(1, 25)]

# ---- page ----
CHORDS = {  # bar -> [(pos, name, root, degree)]
 2:[(0,'C','C','I')], 3:[(0,'G/B','G','V')], 4:[(0,'Am7','A','vi')], 5:[(0,'Am7','A','vi')],
 6:[(0,'Fmaj7','F','IV')], 7:[(0,'G','G','V')], 8:[(0,'C','C','I'),(4,'A7','A','V/ii')], 9:[(0,'Dm7','D','ii')],
 10:[(0,'G','G','V')], 11:[(0,'G7','G','V')], 12:[(0,'Em7','E','iii'),(4,'Am7','A','vi')], 13:[(0,'A7','A','V/ii')],
 14:[(0,'Dm7','D','ii')], 15:[(0,'Dm7','D','ii')], 16:[(0,'G','G','V')], 17:[(0,'G','G','V')],
 18:[(0,'Fmaj7','F','IV'),(4,'Fm','F','iv')], 19:[(0,'Fm','F','iv')], 20:[(0,'Em7','E','iii')],
 21:[(0,'Am7','A','vi'),(6,'A7','A','V/ii')], 22:[(0,'Dm7','D','ii')], 23:[(0,'Dm7','D','ii')], 24:[(0,'G','G','V')],
}
SHOWN = {m: [(p, n, d) for p, n, r, d in v] for m, v in CHORDS.items()}
def chord_at(m, t):
    c = None
    for p, n, r, d in CHORDS.get(m, []):
        if p <= t: c = n
    return c
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
SKIP = set(); TAGS = {}
