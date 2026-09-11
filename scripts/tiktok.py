#!/usr/bin/env python3
# Build/refresh the video list for a TikTok handle into the small JSON that tv.html reads.
# One flat request per handle (extract_flat) — no per-video extraction, so it is fast
# and the least likely thing to trip TikTok's rate limiting on a CI runner.
#
#   python scripts/tiktok.py "tiktokuser:<secUid>" tiktok/teubongday.json "Em Tệu đây"          # newest 30, merged
#   python scripts/tiktok.py "tiktokuser:<secUid>" tiktok/teubongday.json "Em Tệu đây" --all    # every video (one-off, on a PC)
#
# Default runs (the daily Action, update-tiktok.bat) fetch only the newest --limit videos and MERGE them into
# the existing file: new ids go in, known ids get their fresh view counts, nothing is dropped. A one-off
# --all run on a home IP seeds the complete channel; the daily runs then keep it current cheaply.
# If TikTok throttles the IP (200 with an empty body → "Expecting value in ''"), seed from the browser
# instead: scripts/tiktok-seed.browser.js + scripts/tiktok_seed_merge.py (see their headers).
import sys, os, json, time, argparse, datetime
from yt_dlp import YoutubeDL

ap = argparse.ArgumentParser()
ap.add_argument("handle")
ap.add_argument("out")
ap.add_argument("display", nargs="?", default="", help="channel name shown in the app")
ap.add_argument("--all", action="store_true", help="fetch every video instead of the newest --limit")
ap.add_argument("--limit", type=int, default=10, help="newest N videos to fetch (default 10: plenty for a daily run)")
args = ap.parse_args()
handle, out, display = args.handle, args.out, args.display

UTC = datetime.timezone.utc
# Accept a handle ("@name"), a full URL, or yt-dlp's "tiktokuser:<secUid>" scheme (the reliable one:
# TikTok's /@handle page often won't yield the secUid on a server, so we pass the secUid directly).
url = handle if handle.startswith(("http://", "https://", "tiktokuser:")) else "https://www.tiktok.com/" + handle

opts = {
    "quiet": True, "no_warnings": True,
    "extract_flat": True,   # list the videos, don't open each one
    "skip_download": True,
}
if not args.all:
    opts["playlistend"] = args.limit   # newest N

# TikTok throttles unpredictably (a call can return an empty page), which is worse from a datacenter
# IP like a CI runner. Retry a few times with backoff and only accept a page that actually has videos —
# this turns most transient empties into a success within the same run.
ATTEMPTS = 5
info, entries = {}, []
for attempt in range(1, ATTEMPTS + 1):
    try:
        with YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
        entries = info.get("entries") or []
    except Exception as ex:
        print("attempt %d/%d failed: %s" % (attempt, ATTEMPTS, ex))
        entries = []
    if entries:
        print("attempt %d/%d: %d entries" % (attempt, ATTEMPTS, len(entries)))
        break
    if attempt < ATTEMPTS:
        wait = 8 * attempt
        print("attempt %d/%d: empty, retrying in %ds" % (attempt, ATTEMPTS, wait))
        time.sleep(wait)

def best_thumb(e):
    best, bw = "", -1
    for t in (e.get("thumbnails") or []):
        u, w = t.get("url"), (t.get("width") or t.get("preference") or 0)
        if u and w >= bw:
            best, bw = u, w
    return best or e.get("thumbnail") or ""

fresh = []
for e in entries:
    vid = str(e.get("id") or "")
    if not vid:
        continue
    ts = e.get("timestamp")
    fresh.append({
        "id": vid,
        "title": (e.get("title") or "").strip(),
        "thumb": best_thumb(e),
        "dur": int(e.get("duration") or 0),
        "views": int(e.get("view_count") or 0),
        "pub": (datetime.datetime.fromtimestamp(ts, UTC).strftime("%Y-%m-%dT%H:%M:%SZ")) if ts else "",
    })

if not fresh:
    # Never overwrite a good list with an empty one (a blocked/failed scrape must not wipe the app)
    raise SystemExit("no videos extracted for " + handle + " — leaving the existing file untouched")

# Existing file: its title (the tiktokuser:<secUid> form has no readable one) and, unless --all, its videos.
existing = {}
try:
    with open(out, encoding="utf-8") as f:
        existing = json.load(f) or {}
except Exception:
    pass
title = display or info.get("uploader") or info.get("channel") or ""
if not title or title.startswith(("tiktokuser:", "http")):
    title = display or existing.get("title", "") or ""

if args.all:
    videos = fresh
else:
    seen = {v["id"] for v in fresh}
    videos = fresh + [v for v in (existing.get("videos") or []) if v.get("id") not in seen]
    # newest first; entries without a date keep their relative order (stable sort)
    videos.sort(key=lambda v: v.get("pub") or "", reverse=True)
    print("merged: %d fresh + %d kept = %d" % (len(fresh), len(videos) - len(fresh), len(videos)))

data = {
    "handle": handle,
    "title": title,
    "avatar": "",  # the app derives the avatar from the handle (unavatar)
    "updated": datetime.datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "count": len(videos),
    "videos": videos,
}
os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
with open(out, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
print("wrote %d videos to %s" % (len(videos), out))
