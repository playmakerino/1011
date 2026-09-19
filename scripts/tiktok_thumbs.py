"""Download the TikTok thumbnails listed in tiktok/<handle>.json into tiktok/thumbs/<id>.jpg.

TikTok's CDN URLs are signed and expire after ~2 days, so tv.html cannot link them; it links
tiktok/thumbs/<id>.jpg instead. This script fills the folder: for every video without a file it asks
the public oEmbed endpoint for a fresh thumbnail URL, downloads it, shrinks it to 360px wide and
saves a JPEG. Already-present files are skipped, so re-runs only fetch what is new.

    python scripts/tiktok_thumbs.py [--limit N] [--handle teubongday]
"""
import argparse, io, json, sys, time, urllib.request
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
HDR = {"User-Agent": "Mozilla/5.0"}
WIDTH = 360


def fetch(url, timeout=25):
    return urllib.request.urlopen(urllib.request.Request(url, headers=HDR), timeout=timeout).read()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--handle", default="teubongday")
    ap.add_argument("--limit", type=int, default=0, help="stop after N downloads (0 = all)")
    ap.add_argument("--sleep", type=float, default=0.3, help="pause between videos, seconds")
    a = ap.parse_args()

    data = json.loads((ROOT / "tiktok" / f"{a.handle}.json").read_text(encoding="utf-8"))
    out = ROOT / "tiktok" / "thumbs"
    out.mkdir(parents=True, exist_ok=True)
    todo = [v for v in data["videos"] if not (out / f"{v['id']}.jpg").exists()]
    print(f"{len(todo)} missing, {len(data['videos']) - len(todo)} already present", flush=True)
    if a.limit:
        todo = todo[: a.limit]

    ok = fail = 0
    for i, v in enumerate(todo, 1):
        vid = v["id"]
        try:
            oe = f"https://www.tiktok.com/oembed?url=https://www.tiktok.com/@{a.handle}/video/{vid}"
            url = json.loads(fetch(oe))["thumbnail_url"]
            im = Image.open(io.BytesIO(fetch(url))).convert("RGB")
            im.thumbnail((WIDTH, WIDTH * 4))
            buf = io.BytesIO()
            im.save(buf, "JPEG", quality=78, optimize=True)
            (out / f"{vid}.jpg").write_bytes(buf.getvalue())
            ok += 1
        except Exception as e:  # keep going; a re-run picks the missing ones up
            fail += 1
            print(f"  {vid}: {str(e)[:80]}", flush=True)
        if i % 25 == 0 or i == len(todo):
            print(f"{i}/{len(todo)} ok={ok} fail={fail}", flush=True)
        time.sleep(a.sleep)
    print(f"done: ok={ok} fail={fail}", flush=True)
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
