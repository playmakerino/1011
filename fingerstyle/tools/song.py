# Build one song:  python song.py <song> [audit]
#   -> songs/<song>.tg (and songs/<song>_melody.tg when the song has one), ../<song>.html
# A song module (songs/<song>.py) provides:
#   TITLE, TG_NAME, CAPO, TEMPO, STEP (ticks per grid step), BAR (steps per bar), TG, HTML, [MELODY_TG]
#   bars() -> played bars in order (see tablib.build_measures), [melody_bars()]
#   SHOWN {bar: [(pos, chord, degree)]}, chord_at(bar, pos), LABEL, SECTIONS, SKIP, TAGS
import sys, os, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'songs'))
import tablib

name = sys.argv[1]
song = importlib.import_module(name)
bars = tablib.build(song)
if sys.argv[2:] == ['audit']: tablib.audit(song, bars)
else: tablib.page(song, bars)
