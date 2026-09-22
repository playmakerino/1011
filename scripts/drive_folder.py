#!/usr/bin/env python3
"""List a PUBLIC Google Drive folder into the JSON a tv.html "drive" source reads.

No API key, no login: the folder's embedded list view (embeddedfolderview?id=...) is plain HTML with
every file's id and name, and get_video_info?docid=... (also anonymous) gives each video's length.
The page itself cannot do this (neither endpoint sends CORS headers), so the list lives in the repo.

    python scripts/drive_folder.py 1Yyt23fYhQnu3d45EmvsvyWREbjeQ2JpP drive/otgw.json

Output: {"title", "folder", "videos":[{"id","title","dur","subId"?,"subFmt"?}]}  (dur in seconds, 0 if unknown)
Titles drop the extension and a leading "<folder title> - " so cards read "Chapter 1 - ...".
Files are sorted naturally (Chapter 2 before Chapter 10). Run again after adding/replacing files.

Subtitles: a .srt or .vtt file in the same folder with the same name as the video (extension aside,
case-insensitive) is its subtitle; the page fetches it through the Drive API at play time (subId/subFmt).
Caption tracks attached to the file inside Drive are NOT used: drive.google.com/timedtext serves them
without CORS headers, so a page outside google.com cannot read them. The file must be UTF-8.
"""
import html, json, re, sys, urllib.parse, urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
VIDEO_EXT = re.compile(r"\.(mp4|mkv|m4v|mov|webm|avi)$", re.I)
SUB_EXT = re.compile(r"\.(srt|vtt)$", re.I)


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def episode_no(name):
    nums = [int(n) for n in re.findall(r"\d+", name) if not (len(n) == 4 and 1900 <= int(n) <= 2100)]
    return nums[0] if nums else None


def natural_key(s):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", s)]


def length_seconds(file_id):
    try:
        q = urllib.parse.parse_qs(get("https://drive.google.com/get_video_info?docid=" + file_id))
        return int(q.get("length_seconds", ["0"])[0])
    except Exception as e:  # not transcoded yet / quota — the card just shows no duration
        print("  no duration for", file_id, e, file=sys.stderr)
        return 0


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    folder, out = sys.argv[1], sys.argv[2]
    page = get("https://drive.google.com/embeddedfolderview?id=" + folder)
    title = html.unescape(re.search(r"<title>(.*?)</title>", page, re.S).group(1)).strip()
    entries = re.findall(r'id="entry-([\w-]+)".*?<div class="flip-entry-title">(.*?)</div>', page, re.S)
    names = [(fid, html.unescape(name).strip()) for fid, name in entries]
    files = [f for f in names if VIDEO_EXT.search(f[1])]
    subs = {SUB_EXT.sub("", n).lower(): (fid, SUB_EXT.search(n).group(1).lower()) for fid, n in names if SUB_EXT.search(n)}
    # Fallback pairing by episode number (the first number in the name that is not a 4-digit year), for
    # subtitle files named differently from the videos, e.g. "01 - Title.en.srt" for "... - Chapter 1 - Title.mkv".
    by_ep = {}
    for key, sub in subs.items():
        ep = episode_no(key)
        if ep is not None:
            by_ep.setdefault(ep, []).append(sub)
    files.sort(key=lambda f: natural_key(f[1]))
    prefix = title + " - "
    videos = []
    for fid, name in files:
        t = VIDEO_EXT.sub("", name)
        if t.startswith(prefix):
            t = t[len(prefix):]
        v = {"id": fid, "title": t, "dur": length_seconds(fid)}
        sub = subs.get(VIDEO_EXT.sub("", name).lower())
        if not sub:
            cands = by_ep.get(episode_no(name), [])
            sub = cands[0] if len(cands) == 1 else None  # ambiguous numbers pair nothing
        if sub:
            v["subId"], v["subFmt"] = sub
        print(name, "(sub: %s)" % sub[1] if sub else "")
        videos.append(v)
    data = {"title": title, "folder": folder, "videos": videos}
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print("%d videos -> %s" % (len(videos), out))


if __name__ == "__main__":
    main()
