"""Copy each Drive source's card pictures and subtitles into the repo (drive/assets/), so tv.html only
asks the Drive API for the video itself. Every alt=media request counts toward Google's "automated
queries" block on the viewer's IP (a list of 20 cards = 20 requests), and the TV shares the home IP.

For each video in drive/*.json with a thumbId/subId whose local copy is missing, downloads it through
the Drive API (key read from tv.html, sent with the page's Referer since the key is referrer-restricted),
shrinks pictures to 1280 px wide JPEG (the home row shows the first one large), and records the path as "thumbFile"/"subFile" in the JSON.
Runs on a GitHub runner (drive-assets.yml), never from the home IP.
"""
import glob, io, json, os, re, sys, urllib.request
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = "drive/assets"
KEY = re.search(r'const API_KEY = "([^"]+)"', open(os.path.join(ROOT, "tv.html"), encoding="utf-8").read()).group(1)


def fetch(fid):
    req = urllib.request.Request(
        "https://www.googleapis.com/drive/v3/files/%s?alt=media&key=%s" % (fid, KEY),
        headers={"Referer": "https://playmakerino.github.io/1011/tv.html"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def main():
    os.makedirs(os.path.join(ROOT, OUT), exist_ok=True)
    failed = 0
    for path in sorted(glob.glob(os.path.join(ROOT, "drive", "*.json"))):
        data = json.load(open(path, encoding="utf-8"))
        changed = False
        for v in data.get("videos", []):
            jobs = []
            if v.get("thumbId"):
                jobs.append(("thumbFile", "%s/%s.jpg" % (OUT, v["thumbId"]), v["thumbId"], True))
            if v.get("subId"):
                jobs.append(("subFile", "%s/%s.%s" % (OUT, v["subId"], v.get("subFmt") or "srt"), v["subId"], False))
            for field, rel, fid, is_pic in jobs:
                dest = os.path.join(ROOT, rel)
                if not os.path.exists(dest):
                    try:
                        raw = fetch(fid)
                    except Exception as e:
                        print("FAIL %s %s: %s" % (os.path.basename(path), fid, e)); failed += 1; continue
                    if is_pic:
                        im = Image.open(io.BytesIO(raw)).convert("RGB")
                        if im.width > 1280:
                            im = im.resize((1280, round(im.height * 1280 / im.width)), Image.LANCZOS)
                        im.save(dest, "JPEG", quality=82, optimize=True)
                    else:
                        open(dest, "wb").write(raw)
                    print("got %s (%d bytes)" % (rel, os.path.getsize(dest)))
                if v.get(field) != rel:
                    v[field] = rel; changed = True
        if changed:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                json.dump(data, f, ensure_ascii=False, indent=1); f.write("\n")
            print("updated", os.path.basename(path))
    sys.exit(1 if failed else 0)


main()
