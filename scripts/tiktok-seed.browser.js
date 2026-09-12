// Full-channel seed of a TikTok profile when the unsigned API is throttled (yt-dlp gets an empty 200).
// Run in the browser, not from Python: the page's own item_list calls are signed (X-Gnarly/msToken)
// and pass; replaying a captured URL or calling the API from a script gets an empty body.
//
//   1. Open https://www.tiktok.com/@<handle> in Chrome, F12 → Console, paste this whole file, Enter.
//   2. Wait for "done" (about a minute for ~700 videos; it scrolls to the end by itself).
//   3. The dump is copied to the clipboard as JSON → save it as scratch/tt_dump.json.
//   4. python scripts/tiktok_seed_merge.py scratch/tt_dump.json tiktok/<handle>.json
//
// Cards rendered BEFORE this hook was installed (the first page + pinned videos) have no API data;
// they are returned in `missing` with what the DOM shows, and the merge script keeps their entry
// from the existing JSON when there is one (the daily Action already covers the newest ones).
(async () => {
  const TT = (window.__tt = window.__tt || { items: {}, pages: 0, hasMore: null });
  if (!window.__ttHooked) {
    window.__ttHooked = true;
    const add = (txt) => { try { const j = JSON.parse(txt); if (j && j.itemList) { TT.pages++; TT.hasMore = j.hasMore; for (const it of j.itemList) TT.items[it.id] = it; } } catch (e) {} };
    const isList = (u) => String(u || '').includes('/api/post/item_list');
    const of = window.fetch;
    window.fetch = async function (...a) { const r = await of.apply(this, a); try { if (isList(typeof a[0] === 'string' ? a[0] : a[0].url)) r.clone().text().then(add); } catch (e) {} return r; };
    const oo = XMLHttpRequest.prototype.open;
    XMLHttpRequest.prototype.open = function (m, u, ...r) { this.__u = u; return oo.call(this, m, u, ...r); };
    const os = XMLHttpRequest.prototype.send;
    XMLHttpRequest.prototype.send = function (...a) { this.addEventListener('load', () => { if (isList(this.__u)) add(this.responseText); }); return os.apply(this, a); };
  }
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  const cards = () => document.querySelectorAll('[data-e2e="user-post-item"]').length;
  // Only the newest videos are needed for a routine refresh, so stop once TARGET are captured
  // instead of crawling the whole channel (a few seconds vs ~1 min). The merge keeps every
  // older video already in the JSON. Set TARGET = 0 to seed the whole channel (first-time seed).
  const TARGET = 40;
  let last = cards(), stall = 0;
  while (TT.hasMore !== false && stall < 10) {
    if (TARGET && Object.keys(TT.items).length >= TARGET) { console.log('reached TARGET', TARGET, '- stopping'); break; }
    window.scrollTo(0, document.body.scrollHeight);
    await sleep(1200);
    const c = cards();
    stall = c === last ? stall + 1 : 0; last = c;
    console.log('cards', c, 'captured', Object.keys(TT.items).length, 'hasMore', TT.hasMore);
  }
  const iso = (t) => (t ? new Date(t * 1000).toISOString().replace(/\.\d+Z$/, 'Z') : '');
  const data = Object.values(TT.items).map((it) => { const v = it.video || {}, s = it.statsV2 || it.stats || {}; return {
    id: String(it.id), title: (it.desc || '').trim(), thumb: v.cover || v.originCover || '', dur: Number(v.duration || 0),
    views: Number(s.playCount || 0), pub: iso(it.createTime) }; });
  const missing = [];
  document.querySelectorAll('[data-e2e="user-post-item"]').forEach((card) => {
    const a = card.querySelector('a[href*="/video/"]'); const m = a && a.href.match(/\/video\/(\d+)/); if (!m || TT.items[m[1]]) return;
    const img = card.querySelector('img'), vw = card.querySelector('[data-e2e="video-views"]');
    missing.push({ id: m[1], title: (img && img.alt || '').replace(/\s+created by .*$/, '').trim(), thumb: img && img.src || '', views_text: vw && vw.textContent || '' });
  });
  let videoCount = null;
  try { const j = JSON.parse(document.getElementById('__UNIVERSAL_DATA_FOR_REHYDRATION__').textContent); videoCount = j.__DEFAULT_SCOPE__['webapp.user-detail'].userInfo.stats.videoCount; } catch (e) {}
  const dump = { videoCount, n: data.length, missing, data };
  try { copy(JSON.stringify(dump)); console.log('done — dump copied to clipboard'); } catch (e) { console.log('done — copy() unavailable, use: JSON.stringify(window.__ttDump)'); }
  window.__ttDump = dump;
  console.log('captured', data.length, 'missing', missing.length, 'profile says', videoCount);
})();
