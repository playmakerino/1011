# Label color tones inside the tab of laviem.html (hand-made page, no song module), next to the note.
# Pages built by song.py get these labels themselves.
# Chord names on these pages are shape names (capo not counted), so pitches are taken without capo.
# Run again after regenerating a page; it is idempotent.
import re, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
TUNE = [64, 59, 55, 50, 45, 40]
NM = 'C C# D D# E F F# G G# A A# B'.split()
from tablib import COLOR   # same labels as the generated pages
NOTE = re.compile(r'(<text class="tnt (\w+)" x="([\d.]+)" y="([\d.]+)"[^>]*>([^<]*)</text>)(<text class="tiv [^"]*" x="[\d.]+" y="[\d.]+">[^<]*</text>)?')

def fix_svg(svg):
    chords = [(float(x) + 6, n.strip()) for x, n in re.findall(r'<text class="tch" x="([\d.]+)"[^>]*>([^<]*)<tspan', svg)]
    mel_done = set()
    def one(m):
        note, role, x, y, txt, lab = m.groups()
        if role == 'slap' or txt == 'x' or txt.startswith('('): return m.group(0)
        s = round((float(y) - 52.5) / 18) + 1; f = int(txt)
        cur = [n for cx, n in chords if cx <= float(x) + 0.01]
        if not cur or cur[-1] not in COLOR: return m.group(0)
        nm = NM[(TUNE[s - 1] + f) % 12]
        if nm not in COLOR[cur[-1]]: return m.group(0)
        text = COLOR[cur[-1]][nm]
        if role == 'mel':
            if nm in mel_done: return m.group(0)
            mel_done.add(nm)
        if lab: return note + re.sub(r'>[^<]*</text>$', f'>{text}</text>', lab)
        w = 7 * len(txt) + 4
        return note + f'<text class="tiv {role} cl" x="{float(x) + w / 2 + 1:.1f}" y="{float(y) - 1}">{text}</text>'
    return NOTE.sub(one, svg)

def run(path):
    s = open(path, encoding='utf8', newline='').read()
    s = re.sub(r'<span class="tn ctag">[^<]*</span>', '', s)
    s = re.sub(r'<text class="tiv \w+ cl"[^>]*>[^<]*</text>', '', s)
    if '.tiv.mel{' not in s: s = s.replace('</style>', '.tiv.mel{fill:var(--mel)}</style>', 1)
    s = re.sub(r'<svg class="tabsvg".*?</svg>', lambda m: fix_svg(m.group(0)), s, flags=re.S)
    open(path, 'w', encoding='utf8', newline='').write(s)
    print(path, len(re.findall(r'class="tiv \w+ cl"', s)), 'new labels')

for f in sys.argv[1:] or ['laviem.html']:
    run(os.path.join(HERE, '..', f))
