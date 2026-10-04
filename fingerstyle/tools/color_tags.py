# Label color tones inside the tab of laviem.html / mhkcas.html, next to the note (like "root", "5th").
# Chord names on these pages are shape names (capo not counted), so pitches are taken without capo.
# Run again after regenerating a page; it is idempotent.
import re, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
TUNE = [64, 59, 55, 50, 45, 40]
NM = 'C C# D D# E F F# G G# A A# B'.split()
# chord -> {note: (label, any)}: any=True also labels melody notes (tone is in the chord symbol),
# any=False only accompaniment notes (an added color the chord symbol does not have)
COLOR = {
 'C': {'B': ('maj7', False), 'D': ('9th', False), 'A': ('6th', False)},
 'F': {'E': ('maj7', False), 'G': ('9th', False)},
 'Fmaj7': {'E': ('maj7', True), 'G': ('9th', False)},
 'Fm': {'G#': ('b3 mượn', True), 'D': ('6th', False)},
 'G': {'F': ('7th', False), 'A': ('9th', False), 'E': ('6th', False)},
 'G7': {'F': ('7th', True)},
 'Am': {'G': ('7th', False), 'B': ('9th', False)},
 'Am7': {'G': ('7th', True), 'B': ('9th', False)},
 'Em': {'D': ('7th', False)}, 'Em7': {'D': ('7th', True)},
 'Dm7': {'C': ('7th', True), 'E': ('9th', False)},
 'A7': {'C#': ('3rd → D', True), 'G': ('7th', True)},
 'D/F#': {'F#': ('3rd → G', True), 'C': ('7th', False)},
}
COLOR['G/B'] = COLOR['G']; COLOR['Em/G'] = COLOR['Em']
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
        text, anyrole = COLOR[cur[-1]][nm]
        if role != 'mid' and not anyrole: return m.group(0)
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

for f in sys.argv[1:] or ['laviem.html', 'mhkcas.html']:
    run(os.path.join(HERE, '..', f))
