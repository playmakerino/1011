# Shared code for every song: build the TuxGuitar .tg, draw the HTML tab page, audit chord tones.
# A song is a module in tools/songs/ that provides the data (see song.py for the list of fields).
import re, os, zipfile, html

TOOLS = os.path.dirname(os.path.abspath(__file__))
SONGS = os.path.join(TOOLS, 'songs')
PAGES = os.path.dirname(TOOLS)                       # fingerstyle/
TUNE = [64, 59, 55, 50, 45, 40]
Q = 2882880                                          # ticks per quarter note
X = 'x'                                              # slap (dead note)
NM = 'C C# D D# E F F# G G# A A# B'.split()
PC = {n: i for i, n in enumerate(NM)}
PC.update({'Db': 1, 'Eb': 3, 'Gb': 6, 'Ab': 8, 'Bb': 10})
pitch = lambda s, f: TUNE[s - 1] + f

# color tones labelled next to the note in the tab (any role; melody once per bar). Other notes get their interval.
COLOR = {'Fmaj7': {'E': 'maj7'}, 'Fm': {'G#': 'b3 mượn'}, 'Fm6': {'G#': 'b3 mượn', 'D': '6th'},
         'Em7': {'D': '7th'}, 'Am7': {'G': '7th'}, 'Dm7': {'C': '7th'}, 'G7': {'F': '7th'}, 'Cmaj7': {'B': 'maj7'},
         'A7': {'C#': '3rd → D', 'G': '7th', 'A#': 'b9'}, 'D/F#': {'F#': '3rd → G'}}

def root(name):
    return name[:2] if name[1:2] in ('#', 'b') else name[0]

def interval(pc, rt):
    return {0: 'root', 1: 'b9', 2: '9th', 3: '3rd', 4: '3rd', 5: '4th', 6: 'b5', 7: '5th', 8: 'b6', 9: '6th',
            10: '7th', 11: 'maj7'}[(pc - PC[rt]) % 12]

def chord_tones(name):
    q = name.split('/')[0][len(root(name)):]
    iv = {'': (0, 4, 7), 'm': (0, 3, 7), '7': (0, 4, 7, 10), 'maj7': (0, 4, 7, 11), 'm7': (0, 3, 7, 10),
          'm6': (0, 3, 7, 9), '6': (0, 4, 7, 9), 'm7b5': (0, 3, 6, 10), 'sus4': (0, 5, 7)}[q]
    tones = {(PC[root(name)] + i) % 12 for i in iv}
    if '/' in name: tones.add(PC[name.split('/')[1]])
    return tones

# ---------------- .tg ----------------
def note_xml(s, f, vel, tied=False, hammer=False, slide=False, harmonic=False):
    if f == X: return f'<note string="{s}" value="0" velocity="{vel}"><deadNote/></note>'
    a = f'<note string="{s}"' + (' tiedNote="true"' if tied else '') + f' value="{f}" velocity="{vel}"'
    kids = ('<hammer/>' if hammer else '') + ('<slide/>' if slide else '') + ('<harmonic type="N.H" data="0"/>' if harmonic else '')
    return a + (f'>{kids}</note>' if kids else '/>')

def dur_xml(ticks):
    for v in (1, 2, 4, 8, 16, 32):
        base = 4 * Q // v
        if ticks in (base, base * 3 // 2):
            d = ' dotted="dotted"' if ticks != base else ''
            return f'<duration{d} value="{v}"><divisionType enters="1" times="1"/></duration>'
    raise ValueError(ticks)

def split_rest(a, b, bar):
    res = []; t = a
    while t < b:
        k = bar
        while not (t % k == 0 and t + k <= b): k //= 2
        res.append((t, k)); t += k
    return res

def fill_voice(events, bar):          # [(pos, len, xml)] -> {pos: (len, xml)}, rests filled in
    out = {}; t = 0
    for p, ln, nx in sorted(events, key=lambda e: e[0]):
        assert p >= t, ('overlap', p, t)
        for rt, rk in split_rest(t, p, bar): out[rt] = (rk, '')
        out[p] = (ln, nx); t = p + ln
    for rt, rk in split_rest(t, bar, bar): out[rt] = (rk, '')
    return out

EMPTY = '<voice empty="true"><duration value="4"><divisionType enters="1" times="1"/></duration></voice>'

def build_measures(song, bars):
    """bars: played bars in order, each dict(m, mel, h, f, b, vel).
    mel: [dict(pos, len, s, f, tied, hammer, slide)]; h: {pos: [(s,f)]} harmony struck with the melody note;
    f: [(pos, len, [(s,f)])] fills (voice 0); b: [(pos, len, [(s,f)])] voice 1, f == X is a slap;
    vel: (melody, harmony/fill, bass, slap)."""
    step, bar = song.STEP, song.BAR
    # slap goes on the string of the next bass note (same bar, else a later bar); none left -> keep its string
    flat = [(i, k) for i, b in enumerate(bars) for k in range(len(b['b']))]
    for n, (i, k) in enumerate(flat):
        p, ln, ns = bars[i]['b'][k][:3]
        if ns[0][1] != X: continue
        nxt = next((bars[i2]['b'][k2][2] for i2, k2 in flat[n + 1:] if bars[i2]['b'][k2][2][0][1] != X), None)
        if nxt: bars[i]['b'][k] = (p, ln, [(nxt[0][0], X)])
    out, problems = [], []
    for bi, a in enumerate(bars):
        m = a['m']; vm, vh, vb, vs = a['vel']
        ev0, s0, s1 = [], [], []
        for e in a['mel']:
            hs = a['h'].get(e['pos'], [])
            for s, f in hs:
                if pitch(s, f) >= e.get('p', pitch(e['s'], e['f'])): problems.append(f'M{m} harmony above melody at {e["pos"]}')
                if s == e['s']: problems.append(f'M{m} harmony same string as melody at {e["pos"]}')
            fr = [x for x in [e['f']] + [f for _, f in hs] if x > 0]
            if fr and max(fr) - min(fr) > 4: problems.append(f'M{m} stretch at {e["pos"]}')
            nx = note_xml(e['s'], e['f'], vm, e.get('tied'), e.get('hammer'), e.get('slide'), e.get('harm')) + ''.join(note_xml(s, f, vh) for s, f in hs)
            ev0.append((e['pos'], e['len'], nx))
            s0 += [(e['pos'], e['pos'] + e['len'], s) for s in [e['s']] + [s for s, _ in hs]]
        for k in a['h']:
            if k not in [e['pos'] for e in a['mel']]: problems.append(f'M{m} harmony at {k} has no melody note')
        for p, ln, ns in a['f']:
            ev0.append((p, ln, ''.join(note_xml(s, f, vh) for s, f in ns)))
            s0 += [(p, p + ln, s) for s, _ in ns]
        ev1 = []
        mid1 = a.get('mid1', set())       # voice-1 notes that are accompaniment (arpeggio), not bass
        for p, ln, ns in a['b']:
            ev1.append((p, ln, ''.join(note_xml(s, f, vs if f == X else (vh if (p, s, f) in mid1 else vb)) for s, f in ns)))
            s1 += [(p, p + ln, s) for s, f in ns if f != X]
        for a0, b0, x0 in s0:              # same string sounding in both voices at once
            for a1, b1, x1 in s1:
                if x0 == x1 and a0 < b1 and a1 < b0: problems.append(f'M{m} string {x0} clash v0[{a0},{b0}) v1[{a1},{b1})')
        v0, v1 = fill_voice(ev0, bar), fill_voice(ev1, bar)
        rows = []
        for t in sorted(set(v0) | set(v1)):
            def vx(d):
                if t not in d: return EMPTY
                ln, nx = d[t]
                return f'<voice{"" if nx else " empty=\"false\""}>{dur_xml(ln * step)}{nx}</voice>'
            rows.append(f'<TGBeat><preciseStart>{Q + (bi * bar + t) * step}</preciseStart>{vx(v0)}{vx(v1)}</TGBeat>')
        head = '<clef>treble</clef><keySignature>0</keySignature>' if bi == 0 else ''
        out.append('<TGMeasure>' + head + ''.join(rows) + '</TGMeasure>')
    return out, problems

CHANNELS = ('<TGChannel><id>1</id><bank>128</bank><program>0</program><volume>127</volume><balance>64</balance><chorus>0</chorus><reverb>0</reverb><phaser>0</phaser><tremolo>0</tremolo><name>DrumKit</name></TGChannel>'
            '<TGChannel><id>2</id><bank>0</bank><program>25</program><volume>127</volume><balance>64</balance><chorus>0</chorus><reverb>0</reverb><phaser>0</phaser><tremolo>0</tremolo><name>Steel String Acoustic Guitar 1</name></TGChannel>')

def write_tg(song, path, measures):
    hdr = f'<TGMeasureHeader><timeSignature denominator="4" numerator="4"/><tempo>{song.TEMPO}</tempo></TGMeasureHeader>' * len(measures)
    trk = (f'<TGTrack maxFret="29"><name>Track 1</name><channelId>2</channelId><offset>{song.CAPO}</offset><color B="0" G="0" R="255"/>'
           + ''.join(f'<TGString>{p}</TGString>' for p in TUNE) + '<TGLyric from="1"/>' + ''.join(measures) + '</TGTrack>')
    xml = ('<?xml version="1.0" encoding="UTF-8" standalone="no"?><TuxGuitarFile><TGVersion major="2" minor="0" revision="1"/><TGSong>'
           f'<name>{html.escape(song.TG_NAME)}</name><artist/><album/><author/><date/><copyright/><writer/><transcriber/><comments/>'
           + CHANNELS + hdr + trk + '</TGSong></TuxGuitarFile>')
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('version.txt', 'TuxGuitar_file_format 2.0'); z.writestr('content.xml', xml.encode('utf8'))

def read_tg(path, step, bar):
    """-> per measure: list of beats-notes dict(t, v, s, f, tie, dead, hammer, slide), t in song steps."""
    x = zipfile.ZipFile(path).read('content.xml').decode('utf8')
    res = []
    for mi, mx in enumerate(re.findall(r'<TGMeasure>(.*?)</TGMeasure>', x, re.S)):
        ns = []
        for bt in re.findall(r'<TGBeat>(.*?)</TGBeat>', mx, re.S):
            t = (int(re.search(r'<preciseStart>(\d+)', bt).group(1)) - Q) // step - mi * bar
            for vi, (attr, body) in enumerate(re.findall(r'<voice([^>]*)>(.*?)</voice>', bt, re.S)):
                if 'empty="true"' in attr: continue
                d = re.search(r'<duration( dotted="dotted")? value="(\d+)"', body)
                ln = 4 * Q // int(d.group(2)) * (3 if d.group(1) else 2) // 2 // step
                for s, tie, f, _, kids in re.findall(r'<note string="(\d)"( tiedNote="true")? value="(\d+)" velocity="\d+"(/>|>(.*?)</note>)', body):
                    kids = kids or ''
                    ns.append(dict(t=t, len=ln, v=vi, s=int(s), f=int(f), tie=bool(tie), dead='deadNote' in kids,
                                   hammer='hammer' in kids, slide='slide' in kids, harm='<harmonic' in kids))
        res.append(ns)
    return res

def build(song):
    bars = song.bars()
    measures, problems = build_measures(song, bars)
    write_tg(song, song.TG, measures)
    if hasattr(song, 'melody_bars'):
        mm, _ = build_measures(song, song.melody_bars())
        write_tg(song, song.MELODY_TG, mm)
    print('\n'.join(problems) or 'no problems', '| played bars:', len(bars))
    return bars

# ---------------- page ----------------
X0 = 40.5
sy = lambda s: 48 + 18 * (s - 1)

def tab_notes(song, bars):
    """first played copy of each sheet bar -> its notes with a role (mel / mid / bass / slap)."""
    played = read_tg(song.TG, song.STEP, song.BAR)
    for i, a in enumerate(bars):          # roles for every played bar (the bar before is needed for slides)
        mel = {(e['pos'], e['s'], e['f']) for e in a['mel']}
        done = set()
        for n in played[i]:
            if n['v'] == 0 and (n['t'], n['s'], n['f']) in mel and n['t'] not in done:
                n['role'] = 'mel'; done.add(n['t'])
            else:
                n['role'] = 'slap' if n['dead'] else ('mid' if n['v'] == 0 or (n['t'], n['s'], n['f']) in a.get('mid1', ()) else 'bass')
        assert len(done) == len(mel), ('melody not found', a['m'])
    notes, prev = {}, {}
    for i, a in enumerate(bars):
        if a['m'] not in notes:
            for n in played[i]:
                if n['role'] == 'mel' and (n['t'], n['s'], n['f']) in a.get('hide', ()): n['hidden'] = True
            notes[a['m']] = played[i]; prev[a['m']] = played[i - 1] if i else []
    return notes, prev

def bar_svg(song, m, ns, prev):
    DX = 336 / song.BAR
    o = ['<g class="clef"><line class="tbar" x1="0.75" y1="48" x2="0.75" y2="138"/>'
         '<text class="tclef" x="10" y="80" text-anchor="middle">T</text><text class="tclef" x="10" y="98" text-anchor="middle">A</text>'
         '<text class="tclef" x="10" y="116" text-anchor="middle">B</text></g>']
    o.append(f'<text class="tnum" x="2" y="43">{m}</text>')
    for i, c in enumerate('1+2+3+4+'):
        o.append(f'<text class="{"tcnt" if c != "+" else "tcnt2"}" x="{X0 + 42 * i}" y="164" text-anchor="middle">{c}</text>')
    for s in range(1, 7):
        o.append(f'<line class="tstr" x1="0" y1="{sy(s)}" x2="374" y2="{sy(s)}"/>')
    o.append('<line class="tbar" x1="373.25" y1="48" x2="373.25" y2="138"/>')
    for p, name, deg in song.SHOWN.get(m, []):
        o.append(f'<text class="tch" x="{X0 + DX * p - 6:g}" y="30">{html.escape(name)}<tspan class="tdeg"> {deg}</tspan></text>')
    # arcs between consecutive melody notes: h (hammer-on), p (pull-off), s (slide)
    mels = []                             # visible melody notes; a hidden split piece passes its h/p/s to the drawn note
    for n in sorted([n for n in ns if n['role'] == 'mel'], key=lambda n: n['t']):
        if n.get('hidden') and mels:
            mels[-1] = dict(mels[-1], hammer=n['hammer'], slide=n['slide'])
        elif not n.get('hidden'): mels.append(n)
    def arc(x1, x2, y, lab):
        o.append(f'<path class="tslur" d="M{x1:g},{y} Q{(x1 + x2) / 2:g},{y - 9} {x2:g},{y}"/>')
        o.append(f'<text class="tslt" x="{(x1 + x2) / 2:g}" y="{y - 6}" text-anchor="middle">{lab}</text>')
    for a, b in zip(mels, mels[1:]):
        if a['hammer'] or a['slide']:
            up = pitch(b['s'], b['f']) > pitch(a['s'], a['f'])
            arc(X0 + DX * a['t'], X0 + DX * b['t'], min(sy(a['s']), sy(b['s'])) - 8, 's' if a['slide'] else ('h' if up else 'p'))
    pm = sorted([n for n in prev if n['role'] == 'mel'], key=lambda n: n['t'])
    if pm and (pm[-1]['slide'] or pm[-1]['hammer']) and mels and mels[0]['t'] == 0:   # h/p/s across the bar line
        up = pitch(mels[0]['s'], mels[0]['f']) > pitch(pm[-1]['s'], pm[-1]['f'])
        arc(4, X0 + DX * mels[0]['t'], sy(mels[0]['s']) - 8, 's' if pm[-1]['slide'] else ('h' if up else 'p'))
    mel_done = set()                      # melody color tone labelled once per bar
    for n in ns:
        x, y = X0 + DX * n['t'], sy(n['s'])
        if n.get('hidden'): continue      # melody piece split only to strike an accompaniment note: drawn once
        txt = 'x' if n['dead'] else (f"({n['f']})" if n['tie'] else f"<{n['f']}>" if n.get('harm') else str(n['f']))
        w = 7 * len(txt) + 4
        cls = n['role']; label = ''
        ch = song.chord_at(m, n['t'])
        if cls in ('bass', 'mid') and ch and not n['dead']:
            iv = interval(pitch(n['s'], n['f']) % 12, root(ch))
            if cls == 'bass':
                if iv != 'root': cls = 'walk'
                if iv not in ('root', '3rd', '5th'): iv = 'walk'
            label = iv
        nm = NM[pitch(n['s'], n['f']) % 12]
        if ch in COLOR and nm in COLOR[ch] and not n['dead'] and not n['tie'] and not (cls == 'mel' and nm in mel_done):
            label = COLOR[ch][nm]
            if cls == 'mel': mel_done.add(nm)
        o.append(f'<rect class="tmask" x="{x - w / 2:.1f}" y="{y - 6.5}" width="{w}" height="13"/>')
        o.append(f'<text class="tnt {cls}" x="{x:g}" y="{y + 4.5}" text-anchor="middle">{html.escape(txt)}</text>')
        if label:
            o.append(f'<text class="tiv {cls}" x="{x + w / 2 + 1:.1f}" y="{y + 3.5}">{label}</text>')
    return f'<svg class="tabsvg" viewBox="0 15 374 157" role="img" aria-label="tab ô {m}">' + ''.join(o) + '</svg>'

def page(song, bars):
    notes, prev = tab_notes(song, bars)
    lav = open(os.path.join(PAGES, 'laviem.html'), encoding='utf8').read()
    css = lav[lav.index('<style>'):lav.index('</style>')]
    css = css.replace('--mid:#6e8f5a}', '--mid:#6e8f5a;--slap:#475569}')
    css += '.tnt.slap{fill:var(--slap)}' + ('' if '.tiv.mel{' in css else '.tiv.mel{fill:var(--mel)}') + \
           '.tslur{fill:none;stroke:var(--mel);stroke-width:1.2}.tslt{font:italic 700 10px Arial,sans-serif;fill:var(--mel)}\n'
    body = []
    for m in sorted(notes):
        if m in song.SKIP: continue
        if m in song.SECTIONS:
            if body: body.append('</div>')
            body.append(f'<h3 class="sub">{song.SECTIONS[m]}</h3><div class="sys">')
        extra = ''.join(f'<span class="tn">{html.escape(t)}</span>' for t in song.TAGS.get(m, []))
        body.append(f'<div class="bar"><div class="tgs"><span class="tk">{html.escape(song.LABEL[m])}</span>{extra}</div>'
                    + bar_svg(song, m, notes[m], prev[m]) + '</div>')
    body.append('</div>')
    capo = f'<div class="capo">Capo {song.CAPO}</div>\n' if song.CAPO else ''
    out = ('<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n'
           f'<title>{song.TITLE} – tab fingerstyle</title>\n' + css + '</style></head>\n<body>\n<div class="page">\n' + capo
           + ''.join(body) + '</div></body></html>')
    open(song.HTML, 'w', encoding='utf8', newline='\r\n').write(out)
    print('page:', song.HTML, '|', sum(1 for m in notes if m not in song.SKIP), 'bars')

# ---------------- audit ----------------
def audit(song, bars):
    """print every note with its chord; '!' = not a chord tone (melody notes are not flagged)."""
    played = read_tg(song.TG, song.STEP, song.BAR)
    for i, a in enumerate(bars):
        m = a['m']; mel = {(e['pos'], e['s'], e['f']) for e in a['mel']}; lines = []
        for n in played[i]:
            ch = song.chord_at(m, n['t'])
            if n['dead']: lines.append(f"  t{n['t']} v{n['v']} s{n['s']}X"); continue
            p = pitch(n['s'], n['f']); is_mel = n['v'] == 0 and (n['t'], n['s'], n['f']) in mel
            flag = '' if is_mel or not ch or p % 12 in chord_tones(ch) else '!'
            role = 'M' if is_mel else ('B' if n['v'] == 1 else 'h')
            lines.append(f"  t{n['t']} v{n['v']} len{n['len']} [{ch}] {role}:s{n['s']}f{n['f']}={NM[p % 12]}{p // 12 - 1}{flag}{'~' if n['tie'] else ''}")
        print(f'M{m} (played #{i + 1})'); print('\n'.join(lines))
