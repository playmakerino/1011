#!/usr/bin/env python3
"""List a PUBLIC Google Drive folder into the JSON a tv.html "drive" source reads.

No API key, no login: the folder's embedded list view (embeddedfolderview?id=...) is plain HTML with
every file's id and name, and get_video_info?docid=... (also anonymous) gives each video's length.
The page itself cannot do this (neither endpoint sends CORS headers), so the list lives in the repo.

    python scripts/drive_folder.py 1Yyt23fYhQnu3d45EmvsvyWREbjeQ2JpP drive/otgw.json

Output: {"title", "folder", "videos":[{"id","title","dur","sub"?}]}  (dur in seconds, 0 if unknown)
Titles drop the extension and a leading "<folder title> - " so cards read "Chapter 1 - ...".
Files are sorted naturally (Chapter 2 before Chapter 10). Run again after adding/replacing files.

Subtitles: a caption track attached to the file in Drive ("Manage caption tracks") is downloaded as
WebVTT into <out dir>/subs/<id>.vtt and referenced as "sub" (path relative to the site root). It has
to live in the repo: drive.google.com/timedtext serves it without CORS headers, and a cross-origin
<track> needs them. A file with no track in Drive gets no "sub".
"""
import html, json, os, re, sys, urllib.parse, urllib.request

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


def caption_vtt(file_id):
    """WebVTT text of the file's default (else first) caption track, or None."""
    try:
        lst = get("https://drive.google.com/timedtext?id=" + file_id + "&type=list")
        tracks = re.findall(r"<track ([^>]*)/>", lst)
        if not tracks:
            return None
        attrs = [dict(re.findall(r'(\w+)="([^"]*)"', t)) for t in tracks]
        t = next((a for a in attrs if a.get("lang_default") == "true"), attrs[0])
        q = urllib.parse.urlencode({"id": file_id, "type": "track", "lang": t.get("lang_code", "en"),
                                    "name": html.unescape(t.get("name", "")), "fmt": "vtt"})
        vtt = get("https://drive.google.com/timedtext?" + q)
        return vtt if vtt.startswith("WEBVTT") else None
    except Exception as e:
        print("  no caption for", file_id, e, file=sys.stderr)
        return None


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    folder, out = sys.argv[1], sys.argv[2]
    subs_dir = os.path.join(os.path.dirname(out) or ".", "subs")
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
        v = {"id": fid, "title": t, "dur": length_seconds(fid)}
        vtt = caption_vtt(fid)
        if vtt:
            os.makedirs(subs_dir, exist_ok=True)
            with open(os.path.join(subs_dir, fid + ".vtt"), "w", encoding="utf-8", newline="\n") as f:
                f.write(vtt)
            v["sub"] = (os.path.dirname(out).replace(os.sep, "/") + "/subs/" + fid + ".vtt").lstrip("./")
        print(name, "(sub)" if vtt else "")
        videos.append(v)
    data = {"title": title, "folder": folder, "videos": videos}
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print("%d videos -> %s" % (len(videos), out))


if __name__ == "__main__":
    main()
