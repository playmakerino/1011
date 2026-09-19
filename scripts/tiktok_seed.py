#!/usr/bin/env python3
"""Crawl a TikTok profile with a REAL Chrome (driven over CDP) and dump the newest videos.

Why a browser and not yt-dlp / a plain HTTP call: TikTok answers the unsigned /api/post/item_list
with an empty body (yt-dlp) or a 403 (headless Chrome). Only the profile page's OWN item_list
calls are signed (X-Gnarly / msToken) and return data. So we open the page in a real Chrome and
read the responses it makes for itself. On a Linux CI runner Chrome must run under xvfb, NOT
--headless: verified 2026-09-19 that --headless gets 403 while xvfb-run gets 200 on the same IP.

Output is a dump {videoCount, n, missing, data} in the exact shape scripts/tiktok_seed_merge.py
expects, so the merge step is unchanged.

    python scripts/tiktok_seed.py --handle teubongday --target 60 --out scratch/tt_dump.json
"""
import argparse, asyncio, json, os, subprocess, sys, time, urllib.request
import websockets

PORT = 9333


def iso(ts):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(ts)) if ts else ""


def map_item(it):
    v = it.get("video") or {}
    s = it.get("statsV2") or it.get("stats") or {}
    return {
        "id": str(it.get("id")),
        "title": (it.get("desc") or "").strip(),
        "dur": int(v.get("duration") or 0),
        "views": int(s.get("playCount") or 0),
        "pub": iso(it.get("createTime")),
    }


DOM_CARDS_JS = r"""
Array.from(document.querySelectorAll('[data-e2e="user-post-item"]')).map(function(card){
  var a=card.querySelector('a[href*="/video/"]'); var m=a&&a.href.match(/\/video\/(\d+)/); if(!m)return null;
  var img=card.querySelector('img'), vw=card.querySelector('[data-e2e="video-views"]');
  return {id:m[1], title:(img&&img.alt||'').trim(), thumb:img&&img.src||'', views_text:vw&&vw.textContent||''};
}).filter(Boolean)
"""

VIDEOCOUNT_JS = r"""
(function(){try{var j=JSON.parse(document.getElementById('__UNIVERSAL_DATA_FOR_REHYDRATION__').textContent);
return j.__DEFAULT_SCOPE__['webapp.user-detail'].userInfo.stats.videoCount;}catch(e){return null}})()
"""


async def crawl(chrome, handle, target, headless, timeout):
    profile_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chrome-profile")
    args = [chrome, f"--remote-debugging-port={PORT}", f"--user-data-dir={profile_dir}", "--no-first-run",
            "--no-default-browser-check", "--window-size=1280,900", "--lang=vi", "--no-sandbox",
            "--disable-dev-shm-usage"]
    if headless:
        args.append("--headless=new")
    args.append("about:blank")
    p = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        tabs = None
        for _ in range(150):
            try:
                tabs = json.load(urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json"))
                break
            except Exception:
                time.sleep(0.2)
        if not tabs:
            raise RuntimeError("Chrome did not answer on the debug port")
        ws_url = [t for t in tabs if t["type"] == "page"][0]["webSocketDebuggerUrl"]
        async with websockets.connect(ws_url, max_size=None) as ws:
            n = 0

            async def send(method, **params):
                nonlocal n
                n += 1
                await ws.send(json.dumps({"id": n, "method": method, "params": params}))
                return n

            async def result(i):
                while True:
                    b = json.loads(await ws.recv())
                    if b.get("id") == i:
                        return b.get("result", {})

            async def evaluate(expr, by_value=True):
                r = await result(await send("Runtime.evaluate", expression=expr, returnByValue=by_value,
                                            awaitPromise=True))
                return r.get("result", {}).get("value")

            await send("Network.enable")
            await send("Page.enable")
            await send("Page.navigate", url=f"https://www.tiktok.com/@{handle}")

            items, seen, t0, last_count, stall, last_scroll = {}, {}, time.time(), 0, 0, 0.0
            while time.time() - t0 < timeout:
                try:
                    m = json.loads(await asyncio.wait_for(ws.recv(), 3))
                except asyncio.TimeoutError:
                    m = None
                if m and m.get("method") == "Network.responseReceived":
                    r = m["params"]["response"]
                    if "/api/post/item_list" in r["url"]:
                        seen[m["params"]["requestId"]] = r["status"]
                elif m and m.get("method") == "Network.loadingFinished" and m["params"]["requestId"] in seen:
                    rid = m["params"]["requestId"]
                    body = (await result(await send("Network.getResponseBody", requestId=rid))).get("body", "")
                    try:
                        j = json.loads(body)
                        for it in j.get("itemList") or []:
                            items[str(it["id"])] = it
                        print(f"item_list http={seen[rid]} +{len(j.get('itemList') or [])} "
                              f"total={len(items)} hasMore={j.get('hasMore')}", flush=True)
                        if j.get("hasMore") is False:
                            break
                    except Exception:
                        print(f"item_list http={seen[rid]} empty/unparsable ({len(body)} bytes)", flush=True)
                # stop once we have enough, and keep scrolling to pull more pages
                if target and len(items) >= target:
                    break
                now = time.time()
                if now - last_scroll > 1.0:
                    last_scroll = now
                    await send("Runtime.evaluate", expression="window.scrollTo(0,document.body.scrollHeight)")
                    if len(items) == last_count:
                        stall += 1
                        if stall >= 12:  # ~12 s with no new items: end of channel or blocked
                            break
                    else:
                        stall = 0
                    last_count = len(items)

            data = [map_item(it) for it in items.values()]
            cards = await evaluate(DOM_CARDS_JS) or []
            have = {v["id"] for v in data}
            missing = [c for c in cards if c["id"] not in have]
            videocount = await evaluate(VIDEOCOUNT_JS)
            return {"videoCount": videocount, "n": len(data), "target": target, "missing": missing, "data": data}
    finally:
        p.terminate()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--handle", default="teubongday")
    ap.add_argument("--target", type=int, default=60, help="stop after this many API items (0 = whole channel)")
    ap.add_argument("--out", default="scratch/tt_dump.json")
    ap.add_argument("--chrome", default=os.environ.get("CHROME", "/usr/bin/google-chrome"))
    ap.add_argument("--headless", action="store_true", help="works locally; gets 403 on a Linux CI runner")
    ap.add_argument("--timeout", type=int, default=120)
    a = ap.parse_args()

    dump = asyncio.run(crawl(a.chrome, a.handle, a.target, a.headless, a.timeout))
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(dump, f, ensure_ascii=False)
    print(f"wrote {a.out}: {dump['n']} API videos, {len(dump['missing'])} DOM-only, "
          f"profile says {dump['videoCount']}", flush=True)
    return 0 if dump["n"] else 1


if __name__ == "__main__":
    sys.exit(main())
