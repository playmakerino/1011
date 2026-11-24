"""Download the TikTok thumbnails listed in tiktok/<handle>.json into tiktok/thumbs/<id>.webp.

TikTok's CDN URLs are signed and expire after ~2 days, so index.html cannot link them; it links
tiktok/thumbs/<id>.webp instead. This script fills the folder: for every video without a file it takes
the cover URL from a fresh crawl dump (--dump, made by tiktok_seed.py), downloads it, shrinks it to
360px wide and saves a WebP. A video with no cover in the dump counts as failed: crawl again with a
larger --target so the dump reaches it. Already-present files are skipped, so re-runs only fetch what is new.

    python scripts/tiktok_thumbs.py --dump scratch/tt_dump.json [--limit N] [--handle teubongday]
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
    ap.add_argument("--dump", required=True, help="tiktok_seed.py output to take the cover URLs from")
    a = ap.parse_args()

    data = json.loads((ROOT / "tiktok" / f"{a.handle}.json").read_text(encoding="utf-8"))
    dump = json.loads(Path(a.dump).read_text(encoding="utf-8"))
    covers = {m["id"]: m.get("thumb") for m in dump.get("missing") or []}
    covers.update({v["id"]: v.get("cover") for v in dump["data"]})
    out = ROOT / "tiktok" / "thumbs"
    out.mkdir(parents=True, exist_ok=True)
    todo = [v for v in data["videos"] if not (out / f"{v['id']}.webp").exists()]
    print(f"{len(todo)} missing, {len(data['videos']) - len(todo)} already present", flush=True)
    if a.limit:
        todo = todo[: a.limit]

    ok = fail = 0
    for i, v in enumerate(todo, 1):
        vid = v["id"]
        try:
            url = covers.get(vid)
            if not (url or "").startswith("http"):  # a DOM card's img can be a data: placeholder
                raise ValueError("no cover URL in the dump")
            im = Image.open(io.BytesIO(fetch(url))).convert("RGB")
            im.thumbnail((WIDTH, WIDTH * 4))
            buf = io.BytesIO()
            im.save(buf, "WEBP", quality=55, method=6)
            (out / f"{vid}.webp").write_bytes(buf.getvalue())
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
