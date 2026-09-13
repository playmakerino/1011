#!/usr/bin/env python3
# Merge a browser dump (scripts/tiktok-seed.browser.js) into the JSON that tv.html reads.
#   python scripts/tiktok_seed_merge.py scratch/tt_dump.json tiktok/teubongday.json
# Captured items replace the existing entries; `missing` cards (rendered before the hook) keep their
# existing entry when there is one, else go in with what the DOM showed: title, thumb, views parsed
# from "510.2K", dur 0, and the date taken from the id (see iso_from_id) so new videos still sort first.
import sys, re, json, datetime

def iso_from_id(vid):
    # A TikTok video id is a snowflake: the top 32 bits are the unix create time (within seconds of
    # the API's createTime). The first-page cards have no API data, so this is where their date comes from.
    return datetime.datetime.fromtimestamp(int(vid) >> 32, datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def card_title(t):
    # The card's img alt is the caption plus a localized credit: "… created by X" (English UI) or
    # "… do X tạo với bản nhạc …" (Vietnamese UI). Keep only the caption.
    return re.sub(r"\s+(created by|do .+? tạo với) .*$", "", t or "").strip()

def views_from_text(t):
    t = (t or "").strip().upper().replace(",", "")
    mult = {"K": 1e3, "M": 1e6, "B": 1e9}.get(t[-1:], 1)
    try:
        return int(float(t.rstrip("KMB")) * mult)
    except ValueError:
        return 0

dump_path, out = sys.argv[1], sys.argv[2]
dump = json.load(open(dump_path, encoding="utf-8"))
try:
    old = json.load(open(out, encoding="utf-8"))
except Exception:
    old = {"handle": "", "title": "", "avatar": ""}
existing = {v["id"]: v for v in old.get("videos") or []}

KEYS = ["id", "title", "thumb", "dur", "views", "pub"]
videos = {}
for v in dump["data"]:
    videos[v["id"]] = {k: v.get(k, 0 if k in ("dur", "views") else "") for k in KEYS}
partial = []
for m in dump.get("missing") or []:
    # An entry with no date is one a previous merge stored from the DOM alone: rebuild it, don't keep it.
    if m["id"] in existing and existing[m["id"]].get("pub"):
        videos[m["id"]] = existing[m["id"]]
    else:
        videos[m["id"]] = {"id": m["id"], "title": card_title(m.get("title")), "thumb": m.get("thumb", ""), "dur": 0,
                           "views": views_from_text(m.get("views_text")), "pub": iso_from_id(m["id"])}
        partial.append(m["id"])
for vid, v in existing.items():  # never drop a video the file already had
    videos.setdefault(vid, v)

lst = sorted(videos.values(), key=lambda v: v.get("pub") or "", reverse=True)
old.update({
    "updated": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "count": len(lst), "videos": lst,
})
json.dump(old, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote %d videos to %s (profile says %s)" % (len(lst), out, dump.get("videoCount")))
if partial:
    print("no API data for %d (date from id, views from the card, dur 0): %s" % (len(partial), " ".join(partial)))
