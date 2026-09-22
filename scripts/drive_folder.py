#!/usr/bin/env python3
"""List a PUBLIC Google Drive folder into the JSON a tv.html "drive" source reads.

No API key, no login: the folder's embedded list view (embeddedfolderview?id=...) is plain HTML with
every file's id and name, and get_video_info?docid=... (also anonymous) gives each video's length.
The page itself cannot do this (neither endpoint sends CORS headers), so the list lives in the repo.

    python scripts/drive_folder.py 1Yyt23fYhQnu3d45EmvsvyWREbjeQ2JpP drive/otgw.json

Output: {"title", "folder", "videos":[{"id","title","dur"}]}  (dur in seconds, 0 if unknown)
Titles drop the extension and a leading "<folder title> - " so cards read "Chapter 1 - ...".
Files are sorted naturally (Chapter 2 before Chapter 10). Run again after adding/replacing files.
"""
import html, json, re, sys, urllib.parse, urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
VIDEO_EXT = re.compile(r"\.(mp4|mkv|m4v|mov|webm|avi)$", re.I)


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


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
    files = [(fid, html.unescape(name).strip()) for fid, name in entries if VIDEO_EXT.search(name)]
    files.sort(key=lambda f: natural_key(f[1]))
    prefix = title + " - "
    videos = []
    for fid, name in files:
        t = VIDEO_EXT.sub("", name)
        if t.startswith(prefix):
            t = t[len(prefix):]
        print(name)
        videos.append({"id": fid, "title": t, "dur": length_seconds(fid)})
    data = {"title": title, "folder": folder, "videos": videos}
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print("%d videos -> %s" % (len(videos), out))


if __name__ == "__main__":
    main()
