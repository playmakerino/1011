# Shared accompaniment tools (the "bdmt C" principles, see fingerstyle-tab-memory.md -> Nguyên lý soạn phần đệm):
# voice 1 = bass only (ringing until the next bass note or slap); accompaniment notes go to voice 0, struck with a
# melody note (the melody note is split and tied when needed) or as fills in melody rests.
#   parse_lh('0:C3 4:G3') -> [(pos16, midi)]   place() -> accompaniment pitches on the fretboard
#   assemble() -> one bar for tablib             legato() -> re-finger the melody for h/p/s pairs
from tablib import TUNE, X, pitch

NN = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
def note_midi(n):                      # 'C3', 'Bb3', 'F#3'
    return 12 * (int(n[-1]) + 1) + NN[n[0]] + {'b': -1, '#': 1}.get(n[1:2], 0)
def parse_lh(txt):
    return [(int(t), note_midi(n)) for t, n in (tok.split(':') for tok in txt.split())]

BAR = 16                              # grid steps per bar; a song on a 32nd grid sets accomp.BAR = 32
PIECES = (32, 24, 16, 12, 8, 6, 4, 3, 2, 1)
def pieces(n):                        # a length as tied notes TuxGuitar can write
    out = []
    while n:
        k = next(k for k in PIECES if k <= n); out.append(k); n -= k
    return out
def fit(n): return next(k for k in PIECES if k <= n)

def assemble(m, mel, bass, acc, slaps=(), vel=(100, 62, 80, 80), h0=None):
    """mel: melody events of the bar; bass: [(pos, (s,f))]; acc: [(pos, (s,f))] accompaniment notes.
    -> bar dict for tablib, plus dropped notes (reason)."""
    dropped = []
    bass = sorted(bass)            # (pos, (s,f)) or (pos, (s,f), end): rings until the next bass note / slap / end
    stops = sorted([x[0] for x in bass] + list(slaps))
    def nxt_stop(p): return min([q for q in stops if q > p] + [BAR])
    bl = [(x[0], (min(x[2], nxt_stop(x[0])) if len(x) > 2 else nxt_stop(x[0])) - x[0], x[1]) for x in bass]
    cuts = set(p for p, _ in acc) | {e['pos'] for e in mel}
    # split melody notes at accompaniment onsets, then into writable lengths (tied)
    out, hide = [], set()
    for e in mel:
        pts = [e['pos']] + sorted(t for t in cuts if e['pos'] < t < e['pos'] + e['len']) + [e['pos'] + e['len']]
        segs = []
        for a, b in zip(pts, pts[1:]):
            t = a
            for k in pieces(b - a): segs.append((t, k)); t += k
        for i, (t, k) in enumerate(segs):
            last = i == len(segs) - 1      # hammer/slide belong to the last piece (they lead into the next note)
            out.append(dict(e, pos=t, len=k, tied=e['tied'] if i == 0 else True, tie_out=e['tie_out'] if last else True,
                            hammer=e.get('hammer') and last, slide=e.get('slide') and last))
            if i: hide.add((t, e['s'], e['f']))
    mel = out
    def mel_at(t): return next((e for e in mel if e['pos'] <= t < e['pos'] + e['len']), None)
    h, fills = {k: list(v) for k, v in (h0 or {}).items()}, []
    starts = sorted({e['pos'] for e in mel} | set(p for p, _ in acc))
    for t, (s, f) in sorted(acc):
        e = mel_at(t); p = pitch(s, f)
        if e is not None:
            if p >= e['p']: dropped.append((m, t, p, 'not below melody')); continue
            if s == e['s']: dropped.append((m, t, p, 'melody string')); continue
            if e['pos'] != t: dropped.append((m, t, p, 'inside a melody note')); continue
            if any(s2 == s for s2, _ in h.get(t, [])): dropped.append((m, t, p, 'string taken')); continue
            h.setdefault(t, []).append((s, f))
        else:
            nxt = min([x for x in starts if x > t] + [BAR])
            if any(p0 == t and s2 == s for p0, _, ns in fills for s2, _ in ns): dropped.append((m, t, p, 'string taken')); continue
            same = [x for x in fills if x[0] == t]
            if same: same[0][2].append((s, f))
            else: fills.append((t, fit(nxt - t), [(s, f)]))
    # a bass note stops when its string is struck again in voice 0
    v0 = [(t, t + e['len'], s) for e in mel for t, s in [(e['pos'], e['s'])]] + \
         [(t, t + next(e['len'] for e in mel if e['pos'] == t), s) for t, ns in h.items() for s, _ in ns] + \
         [(t, t + ln, s) for t, ln, ns in fills for s, _ in ns]
    b = []
    for p, ln, (s, f) in bl:
        if any(s0 == s and a <= p < z for a, z, s0 in v0):
            dropped.append((m, p, pitch(s, f), 'bass string sounding in melody')); continue
        end = min([a for a, z, s0 in v0 if s0 == s and p < a < p + ln] + [p + ln])
        b.append((p, fit(end - p), [(s, f)]))
    for p in slaps:               # slap: string set by tablib (string of the next bass note)
        b.append((p, fit(nxt_stop(p) - p), [(6, X)]))
    b.sort(key=lambda x: x[0])
    return dict(m=m, mel=mel, h=h, f=fills, b=b, mid1=set(), hide=hide, vel=vel), dropped


def cands(p, strings=range(6, 0, -1)):
    return [(s, p - TUNE[s - 1]) for s in strings if 0 <= p - TUNE[s - 1] <= 12]

def place(m, ev, bass, notes, dropped, octave=None, pos_ovr=None, span=4, low=None):
    """notes: [(pos, midi)] accompaniment pitches -> [(pos, (s,f))] on the fretboard.
    A note at/above the melody goes down an octave; same note as the ringing bass is dropped; the string is
    chosen near the melody's fret, avoiding the melody string and the ringing bass string."""
    pos_ovr = pos_ovr or {}
    def mel_at(t): return next((e for e in ev if e['pos'] <= t < e['pos'] + e['len']), None)
    acc, used = [], {}
    for t, p in notes:
        e = mel_at(t)
        if e and p >= e['p']:
            if p - 12 >= e['p'] or p - 12 < 40: dropped.append((m, t, p, 'above melody')); continue
            p -= 12
            if octave is not None: octave.append((m, t))
        rb = [x for x in sorted(bass) if x[0] <= t][-1:]
        if rb and pitch(*rb[0][1]) == p and (len(rb[0]) < 3 or rb[0][2] > t):
            dropped.append((m, t, p, 'same note ringing in the bass')); continue
        ringing = [x[1][0] for x in rb]
        if any(pitch(*sf) == p for t2, sf in acc if t2 == t):
            dropped.append((m, t, p, 'same note already struck')); continue
        def cost(sf):
            s, f = sf
            fr = [x for x in [e['f'] if e else 0] + [x[1][1] for x in rb] + [f2 for t2, (s2, f2) in acc if t2 == t] if x] if f else []
            st = max([abs(f - x) for x in fr] + [0])          # stretch against the melody and the ringing bass
            return (s in ringing) * 10 + max(0, st - span) * 20 + f * 0.1 + (max(0, f - low) * 3 if low is not None else 0)
        c = [sf for sf in cands(p) if not (e and sf[0] == e['s']) and sf[0] not in used.get(t, ())]
        if (m, t, p) in pos_ovr: c = [pos_ovr[(m, t, p)]]
        if not c: dropped.append((m, t, p, 'no string')); continue
        sf = min(c, key=cost)
        if cost(sf) >= 20: dropped.append((m, t, p, 'stretch')); continue
        used.setdefault(t, set()).add(sf[0]); acc.append((t, sf))
    return acc

def legato(seq, keep=1.0, max_fret=5, max_leg=2):
    """Re-finger a melody to get as many hammer-ons / pull-offs / slides as possible.
    seq: melody events of the whole song in play order, each with 'bar' (index) added. Chooses (s,f) per note by DP:
    +3 per legato pair (pairs only: a note reached by legato does not start another), -keep for leaving the original position, -0.3 per fret of a jump beyond 4 frets.
    Legato pair = consecutive notes (no rest), same string, second note not tied, 1..max_leg frets apart -> h/p
    (the user: at most 2 frets, no slides). h/p across a bar line is allowed (drawn from the bar line). Sets e['s'], e['f'], e['hammer'], e['slide']."""
    def opts(e):
        if e.get('harm') or e.get('lock'): return [(e['s0'], e['f0'])]
        top = max(max_fret, e['f0'])        # stay in the low position unless the note already sits higher
        return [(s, e['p'] - TUNE[s - 1]) for s in (1, 2, 3, 4, 5, 6) if 0 <= e['p'] - TUNE[s - 1] <= top]
    def kind(a, sa, b, sb):
        if sa[0] != sb[0] or b['tied'] or a.get('harm') or b.get('harm') or a['end'] != b['start'] or a['p'] == b['p']: return None
        d = abs(sa[1] - sb[1])
        return 'h' if 1 <= d <= max_leg else None    # hammer-on / pull-off only, at most max_leg frets
    def move(sa, sb):
        if not sa[1] or not sb[1]: return 0
        return max(0, abs(sa[1] - sb[1]) - 4) * 0.3
    # DP state = (position, reached by legato?): a note reached by legato cannot start another one (pairs only)
    best = []
    for i, e in enumerate(seq):
        pen = lambda sf: keep if sf != (e['s0'], e['f0']) else 0
        cur = {}
        if i == 0:
            for sf in opts(e): cur[(sf, False)] = (-pen(sf), None)
        else:
            prev = best[-1]
            for sf in opts(e) if not e['tied'] else {k[0] for k in prev}:
                for st, (sc, _) in prev.items():
                    sp, inleg = st
                    if e['tied'] and sp != sf: continue
                    k = kind(seq[i - 1], sp, e, sf) and not inleg
                    key = (sf, inleg if e['tied'] else bool(k))   # a tie continues the same sounding note
                    v = (sc + (3 if k else 0) - move(sp, sf) - pen(sf), st)
                    if key not in cur or v[0] > cur[key][0]: cur[key] = v
        best.append(cur)
    st = max(best[-1], key=lambda k: best[-1][k][0]); path = [st]
    for i in range(len(seq) - 1, 0, -1):
        st = best[i][st][1]; path.append(st)
    path.reverse()
    for e, (sf, _) in zip(seq, path): e['s'], e['f'] = sf; e['hammer'] = e['slide'] = False
    n = {'h': 0, 's': 0}
    for a, b, (sa, _), (sb, leg) in zip(seq, seq[1:], path, path[1:]):
        if not leg or b['tied']: continue
        k = kind(a, sa, b, sb)
        if k == 'h': a['hammer'] = True; n['h'] += 1
        if k == 's': a['slide'] = True; n['s'] += 1
    return n
