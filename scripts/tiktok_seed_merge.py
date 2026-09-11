#!/usr/bin/env python3
# Merge a browser dump (scripts/tiktok-seed.browser.js) into the JSON that tv.html reads.
#   python scripts/tiktok_seed_merge.py scratch/tt_dump.json tiktok/teubongday.json
# Captured items replace the existing entries; `missing` cards (rendered before the hook) keep their
# existing entry when there is one, else go in with what the DOM showed (dur 0, no date → sorted last).
import sys, json, datetime

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
    if m["id"] in existing:
        videos[m["id"]] = existing[m["id"]]
    else:
        videos[m["id"]] = {"id": m["id"], "title": m.get("title", ""), "thumb": m.get("thumb", ""), "dur": 0, "views": 0, "pub": ""}
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
    print("no API data for %d (open each video page to fill dur/views/pub): %s" % (len(partial), " ".join(partial)))
