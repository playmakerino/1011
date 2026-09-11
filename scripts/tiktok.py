#!/usr/bin/env python3
# Build the video list for a TikTok handle into the small JSON that tv.html reads.
# One flat request per handle (extract_flat) — no per-video extraction, so it is fast
# and the least likely thing to trip TikTok's rate limiting on a CI runner.
#   python scripts/tiktok.py "tiktokuser:<secUid>" tiktok/teubongday.json "Em Tệu đây"
import sys, os, json, datetime
from yt_dlp import YoutubeDL

UTC = datetime.timezone.utc
handle, out = sys.argv[1], sys.argv[2]
display = sys.argv[3] if len(sys.argv) > 3 else ""  # channel name shown in the app
LIMIT = 40  # newest N videos
# Accept a handle ("@name"), a full URL, or yt-dlp's "tiktokuser:<secUid>" scheme (the reliable one:
# TikTok's /@handle page often won't yield the secUid on a server, so we pass the secUid directly).
if handle.startswith(("http://", "https://", "tiktokuser:")):
    url = handle
else:
    url = "https://www.tiktok.com/" + handle

opts = {
    "quiet": True, "no_warnings": True,
    "extract_flat": True,   # list the videos, don't open each one
    "playlistend": LIMIT,   # newest N
    "skip_download": True,
}
with YoutubeDL(opts) as ydl:
    info = ydl.extract_info(url, download=False)
entries = info.get("entries") or []

def best_thumb(e):
    best, bw = "", -1
    for t in (e.get("thumbnails") or []):
        u, w = t.get("url"), (t.get("width") or t.get("preference") or 0)
        if u and w >= bw:
            best, bw = u, w
    return best or e.get("thumbnail") or ""

videos = []
for e in entries:
    vid = str(e.get("id") or "")
    if not vid:
        continue
    ts = e.get("timestamp")
    videos.append({
        "id": vid,
        "title": (e.get("title") or "").strip(),
        "thumb": best_thumb(e),
        "dur": int(e.get("duration") or 0),
        "views": int(e.get("view_count") or 0),
        "pub": (datetime.datetime.fromtimestamp(ts, UTC).strftime("%Y-%m-%dT%H:%M:%SZ")) if ts else "",
    })

if not videos:
    # Never overwrite a good list with an empty one (a blocked/failed scrape must not wipe the app)
    raise SystemExit("no videos extracted for " + handle + " — leaving the existing file untouched")

# The tiktokuser:<secUid> form has no readable title, so prefer the display name passed in.
title = display or info.get("uploader") or info.get("channel") or ""
if not title or title.startswith(("tiktokuser:", "http")):
    title = display or ""

data = {
    "handle": handle,
    "title": title,
    "avatar": "",  # channel avatar isn't reliably present in flat mode
    "updated": datetime.datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "count": len(videos),
    "videos": videos,
}
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
print("wrote %d videos to %s" % (len(videos), out))
