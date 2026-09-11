package io.github.playmakerino.tv;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.Gravity;
import android.view.KeyEvent;
import android.view.View;
import android.view.ViewGroup;
import android.view.WindowManager;
import android.webkit.JavascriptInterface;
import android.webkit.RenderProcessGoneDetail;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceError;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.TextView;

import org.json.JSONObject;
import org.json.JSONTokener;

import java.io.ByteArrayInputStream;

public class MainActivity extends Activity {
    private static final String URL = "https://playmakerino.github.io/1011/tv.html";
    private static final String HOST = "playmakerino.github.io";
    private static final int BG = 0xFF0F0F0F;

    private FrameLayout root;
    private WebView web;
    private LinearLayout offline;
    private Button retryBtn;
    private boolean loadFailed;
    private View fullscreenView;
    private WebChromeClient.CustomViewCallback fullscreenCallback;
    private final Handler ui = new Handler(Looper.getMainLooper());

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);

        root = new FrameLayout(this);
        root.setBackgroundColor(BG);
        setContentView(root);
        createWebView();
        createOfflineView();
        immersive(); // the page is always edge-to-edge; it no longer asks for fullscreen itself

        if (savedInstanceState == null || web.restoreState(savedInstanceState) == null) web.loadUrl(URL);
    }

    private static FrameLayout.LayoutParams fill() {
        return new FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT);
    }

    @SuppressLint({"SetJavaScriptEnabled", "AddJavascriptInterface"})
    private void createWebView() {
        web = new WebView(this);
        web.setBackgroundColor(BG);
        web.setFocusable(true);
        web.setFocusableInTouchMode(true);

        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);           // tv.html caches its lists in localStorage
        s.setMediaPlaybackRequiresUserGesture(false);
        s.setLoadWithOverviewMode(true);
        s.setUseWideViewPort(true);
        s.setSupportZoom(false);
        s.setTextZoom(100);                     // ignore the system font-size setting so the layout stays as designed
        // tv.html checks for this tag: inside the app it skips requestFullscreen (the WebView fullscreen
        // transition re-creates the video surface and costs a black re-layout on every open).
        s.setUserAgentString(s.getUserAgentString() + " TVApp/1");

        web.addJavascriptInterface(new Bridge(), "TVApp"); // tv.html -> TikTok player (see below)
        web.setWebViewClient(new Client());
        web.setWebChromeClient(new Chrome());
        root.addView(web, 0, fill());
        web.requestFocus();
    }

    private void createOfflineView() {
        offline = new LinearLayout(this);
        offline.setOrientation(LinearLayout.VERTICAL);
        offline.setGravity(Gravity.CENTER);
        offline.setBackgroundColor(BG);
        TextView t = new TextView(this);
        t.setText("Can't reach the page. Check the network.");
        t.setTextSize(20);
        t.setTextColor(0xFFF1F1F1);
        t.setPadding(0, 0, 0, 32);
        retryBtn = new Button(this);
        retryBtn.setText("Retry");
        retryBtn.setOnClickListener(v -> { retryBtn.setText("Retrying…"); web.loadUrl(URL); });
        offline.addView(t);
        offline.addView(retryBtn);
        offline.setVisibility(View.GONE);
        root.addView(offline, fill());
    }

    private void showOffline() {
        loadFailed = true;
        retryBtn.setText("Retry");
        offline.setVisibility(View.VISIBLE);
        retryBtn.requestFocus();
    }

    private class Client extends WebViewClient {
        // Only this site may ever replace the page. The YouTube logo / title inside the embedded player
        // would otherwise open youtube.com itself in the app, which defeats the whitelist. (API 24+;
        // the embedded player's own sub-frame navigations are not routed through here.)
        @Override
        public boolean shouldOverrideUrlLoading(WebView v, WebResourceRequest req) {
            if (!req.isForMainFrame()) return false;
            Uri u = req.getUrl();
            return u == null || !HOST.equalsIgnoreCase(u.getHost());
        }

        @Override
        public void onPageStarted(WebView v, String url, Bitmap favicon) { loadFailed = false; }

        @Override
        public void onPageFinished(WebView v, String url) {
            if (loadFailed || offline.getVisibility() != View.VISIBLE) return;
            offline.setVisibility(View.GONE);
            web.clearHistory(); // drop the failed attempt so Back does not land on an error page
            web.requestFocus();
        }

        @Override // API 23+
        public void onReceivedError(WebView v, WebResourceRequest req, WebResourceError err) {
            if (req.isForMainFrame()) showOffline();
        }

        @SuppressWarnings("deprecation")
        @Override // API < 23 only
        public void onReceivedError(WebView v, int code, String desc, String failingUrl) {
            if (failingUrl != null && failingUrl.startsWith(URL)) showOffline();
        }

        @Override // API 26+
        public boolean onRenderProcessGone(WebView v, RenderProcessGoneDetail detail) {
            // The renderer was killed (low memory on TV boxes). Default behaviour would kill the app;
            // instead throw the dead WebView away and start over.
            if (v != web) return true;
            root.removeView(web);
            web.destroy();
            if (fullscreenView != null) { root.removeView(fullscreenView); fullscreenView = null; fullscreenCallback = null; }
            createWebView();
            web.loadUrl(URL);
            return true;
        }
    }

    private class Chrome extends WebChromeClient {
        @Override
        public void onShowCustomView(View view, CustomViewCallback callback) {
            if (fullscreenView != null) { callback.onCustomViewHidden(); return; }
            fullscreenView = view;
            fullscreenCallback = callback;
            web.setVisibility(View.GONE);
            root.addView(view, fill());
            immersive();
        }

        @Override
        public void onHideCustomView() {
            if (fullscreenView == null) return;
            root.removeView(fullscreenView);
            fullscreenView = null;
            web.setVisibility(View.VISIBLE);
            immersive();
            if (fullscreenCallback != null) { fullscreenCallback.onCustomViewHidden(); fullscreenCallback = null; }
        }
    }

    private void immersive() {
        getWindow().getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_FULLSCREEN | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY | View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION);
    }

    @Override
    public void onWindowFocusChanged(boolean hasFocus) {
        super.onWindowFocusChanged(hasFocus);
        if (hasFocus) immersive(); // system bars come back after a dialog/notification; hide them again
    }

    // Media buttons on TV remotes are not forwarded to the page as key events by WebView;
    // hand them to tv.html's window.tvKey(name) so seeking / play-pause works.
    @Override
    public boolean dispatchKeyEvent(KeyEvent ev) {
        if (ttVisible && ttKey(ev)) return true; // the TikTok player is on top: the remote drives it
        if (ev.getAction() == KeyEvent.ACTION_DOWN && web != null) {
            String k = null;
            switch (ev.getKeyCode()) {
                case KeyEvent.KEYCODE_MEDIA_PLAY_PAUSE: k = "MediaPlayPause"; break;
                case KeyEvent.KEYCODE_MEDIA_PLAY: k = "MediaPlay"; break;
                case KeyEvent.KEYCODE_MEDIA_PAUSE: k = "MediaPause"; break;
                case KeyEvent.KEYCODE_MEDIA_REWIND: k = "MediaRewind"; break;
                case KeyEvent.KEYCODE_MEDIA_FAST_FORWARD: k = "MediaFastForward"; break;
                case KeyEvent.KEYCODE_MEDIA_STOP: k = "MediaStop"; break;
            }
            if (k != null) {
                web.evaluateJavascript("window.tvKey&&tvKey('" + k + "')", null);
                return true;
            }
        }
        return super.dispatchKeyEvent(ev);
    }

    @Override
    public void onBackPressed() {
        if (ttVisible) { ttClose(); return; }
        if (fullscreenView != null) {
            web.evaluateJavascript("document.exitFullscreen&&document.exitFullscreen()", null);
            return;
        }
        if (web.canGoBack()) { web.goBack(); return; } // tv.html keeps an entry for the open player, so Back closes it first
        super.onBackPressed();
    }

    @Override protected void onSaveInstanceState(Bundle out) { super.onSaveInstanceState(out); web.saveState(out); }
    @Override protected void onPause() { super.onPause(); web.onPause(); if (tt != null) tt.onPause(); }
    @Override protected void onResume() { super.onResume(); web.onResume(); if (tt != null) tt.onResume(); }
    @Override protected void onDestroy() { if (tt != null) tt.destroy(); web.destroy(); super.onDestroy(); }

    // ======================= TikTok player =======================
    // TikTok's embed player picks an H.265 stream that TV boxes can't decode (picture frozen, audio
    // stalls). Every video page also embeds its stream list in the HTML, including an H.264 one. So a
    // second WebView loads the video page (a real browser passes TikTok's bot check and holds the
    // session cookies the CDN wants), we read that list before TikTok's own scripts matter, stop the
    // page, and replace it with a bare <video> on the H.264 URL. Same origin, so the CDN serves it;
    // Chromium decodes H.264 in hardware; the remote drives it through evaluateJavascript.
    private WebView tt;
    private boolean ttVisible;
    private String ttLoadingId, ttReadyId, ttUser;
    private boolean ttPlayWhenReady;
    // 1: the TikTok video page is loading (we poll it for the stream URL); 2: our own blank page (origin
    // tiktok.com via loadDataWithBaseURL) is loading; 3: the bare player is in place. While >= 2 every
    // navigation is blocked — TikTok's SPA otherwise redirects/reloads and takes the WebView back.
    private int ttStage;
    private String ttFoundUrl;
    private long ttDeadline;                                         // uptime ms; a challenge reload can't extend it
    private static final int TT_POLL_MS = 200, TT_TIMEOUT_MS = 20000; // for the page, bot challenge included

    // Called from tv.html (runs on a WebView thread; hop to the UI thread).
    private class Bridge {
        @JavascriptInterface public void playTikTok(String id, String user) { if (ok(id, user)) ui.post(() -> ttLoad(id, user, true)); }
        @JavascriptInterface public void prefetchTikTok(String id, String user) { if (ok(id, user)) ui.post(() -> { if (!ttVisible) ttLoad(id, user, false); }); }
        @JavascriptInterface public void closeTikTok() { ui.post(MainActivity.this::ttClose); }
        private boolean ok(String id, String user) { return id != null && user != null && id.matches("\\d{5,25}") && user.matches("[\\w.\\-]{1,64}"); }
    }

    // Called from the injected player page (video events).
    private class TtBridge {
        @JavascriptInterface public void event(String ev) { ui.post(() -> ttEvent(ev)); }
    }

    @SuppressLint({"SetJavaScriptEnabled", "AddJavascriptInterface"})
    private void ttCreate() {
        tt = new WebView(this);
        tt.setBackgroundColor(0xFF000000);
        tt.setFocusable(true);
        tt.setFocusableInTouchMode(true);
        WebSettings s = tt.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setMediaPlaybackRequiresUserGesture(false); // play() comes from evaluateJavascript, not a tap
        s.setSupportZoom(false);
        tt.addJavascriptInterface(new TtBridge(), "TVNative");
        tt.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView v, WebResourceRequest req) {
                if (!req.isForMainFrame()) return false;
                if (ttStage >= 2) return true; // player page in place: nothing may navigate it away
                Uri u = req.getUrl(); String h = u == null ? "" : String.valueOf(u.getHost());
                return !(h.endsWith("tiktok.com")) && !"about:blank".equals(String.valueOf(u));
            }
            @Override // images/fonts/analytics only slow the page down; the stream list is in the HTML itself
            public WebResourceResponse shouldInterceptRequest(WebView v, WebResourceRequest req) {
                if (req.isForMainFrame()) return null;
                String u = String.valueOf(req.getUrl()).toLowerCase();
                String p = u.split("\\?")[0];
                boolean block = p.matches(".*\\.(png|jpe?g|webp|gif|svg|ico|woff2?|ttf|otf|mp3|m4a)$")
                        || u.contains("/monitor_browser/") || u.contains("/report/") || u.contains("mcs.tiktok") || u.contains("mon.tiktok")
                        || u.contains("p16-") || u.contains("p19-") || u.contains("-sign-va") || u.contains("-sign-sg");
                return block ? new WebResourceResponse("text/plain", "utf-8", new ByteArrayInputStream(new byte[0])) : null;
            }
            @Override
            public void onPageStarted(WebView v, String url, Bitmap favicon) {
                // any navigation while the video page loads (challenge reload, redirect): keep polling
                if (ttLoadingId != null && ttStage == 1) { ui.removeCallbacks(ttPoll); ui.postDelayed(ttPoll, 50); }
                if (ttStage >= 2) notifyPage("dbg:start " + url);
            }
            @Override
            public void onPageFinished(WebView v, String url) {
                if (ttStage >= 2) notifyPage("dbg:finish " + url);
                if (ttStage != 2 || ttLoadingId == null || ttFoundUrl == null) return;
                // our player document (tiktok.com origin, script inlined) is up
                ttStage = 3;
                ttReadyId = ttLoadingId; ttLoadingId = null;
                if (ttPlayWhenReady) ttShow();
            }
            @Override
            public void onReceivedError(WebView v, WebResourceRequest req, WebResourceError err) {
                if (req.isForMainFrame() && ttLoadingId != null) ttFail("network");
            }
            @Override
            public boolean onRenderProcessGone(WebView v, RenderProcessGoneDetail detail) {
                if (v != tt) return true;
                root.removeView(tt); tt.destroy(); tt = null;
                boolean wasVisible = ttVisible;
                ttVisible = false; ttLoadingId = ttReadyId = null; ttStage = 0; ttFoundUrl = null;
                web.setVisibility(View.VISIBLE);
                if (wasVisible) { web.requestFocus(); notifyPage("closed"); }
                return true;
            }
        });
        tt.setVisibility(View.GONE);
        root.addView(tt, fill()); // above the main WebView (index 0), below the offline view
    }

    private void ttLoad(String id, String user, boolean play) {
        if (tt == null) ttCreate();
        ttPlayWhenReady = play;
        if (id.equals(ttReadyId)) { if (play) ttShow(); return; }   // prefetched: instant
        if (id.equals(ttLoadingId)) { if (play) notifyPage("loading"); return; } // already on its way
        ui.removeCallbacks(ttPoll);
        ttLoadingId = id; ttReadyId = null; ttUser = user;
        if (play) notifyPage("loading");
        // The two scripts run in the TikTok WebView live in tv.html (window.TT_EXTRACT_JS / TT_PLAYER_JS):
        // a TikTok page change is fixed by editing the page, never by rebuilding the app. The app holds
        // no copy of its own — one source of truth.
        web.evaluateJavascript("JSON.stringify({e:String(window.TT_EXTRACT_JS||''),p:String(window.TT_PLAYER_JS||''),ua:String(window.TT_UA||''),d:String(window.TT_DIAG_JS||'')})", res -> {
            ttExtractJs = ttPlayerJs = ttDiagJs = null; String ua = "";
            try {
                Object o = new JSONTokener(res == null ? "null" : res).nextValue();
                if (o instanceof String) {
                    JSONObject j = new JSONObject((String) o);
                    ttExtractJs = j.optString("e", ""); ttPlayerJs = j.optString("p", ""); ttDiagJs = j.optString("d", ""); ua = j.optString("ua", "");
                }
            } catch (Exception ignored) {}
            if (!id.equals(ttLoadingId) || tt == null) return; // superseded meanwhile
            if (ttExtractJs == null || ttExtractJs.isEmpty() || ttPlayerJs == null || ttPlayerJs.isEmpty()) { ttFail("page has no TT scripts"); return; }
            // the page decides what browser TikTok sees (TV WebView UAs get challenge/unsupported pages)
            if (!ua.isEmpty()) tt.getSettings().setUserAgentString(ua);
            ttDeadline = android.os.SystemClock.uptimeMillis() + TT_TIMEOUT_MS;
            ttStage = 1; ttFoundUrl = null;
            tt.loadUrl("https://www.tiktok.com/@" + user + "/video/" + id);
            ui.removeCallbacks(ttPoll); ui.postDelayed(ttPoll, 300);
        });
    }
    private String ttExtractJs, ttPlayerJs, ttDiagJs; // fetched from tv.html per load (see ttLoad)

    // Failure with a one-line description of what the TikTok WebView is showing (tv.html's TT_DIAG_JS),
    // readable on the TV where there is no console.
    private void ttFailDiag(String why) {
        if (tt == null || ttDiagJs == null || ttDiagJs.isEmpty()) { ttFail(why); return; }
        tt.evaluateJavascript(ttDiagJs, r -> {
            String d = "";
            try { Object o = new JSONTokener(r == null ? "null" : r).nextValue(); d = o == null ? "" : o.toString(); } catch (Exception ignored) {}
            ttFail(why + (d.isEmpty() ? "" : " | " + d));
        });
    }


    private final Runnable ttPoll = new Runnable() {
        @Override public void run() {
            if (tt == null || ttLoadingId == null) return;
            final String id = ttLoadingId;
            tt.evaluateJavascript(ttExtractJs, res -> {
                if (!id.equals(ttLoadingId)) return; // a newer load replaced this one
                String r;
                try { Object o = new JSONTokener(res == null ? "null" : res).nextValue(); r = o == null ? "WAIT" : o.toString(); }
                catch (Exception e) { r = "WAIT"; }
                if (r.startsWith("{")) {
                    String url;
                    try { url = new JSONObject(r).getString("url"); } catch (Exception e) { ttFail("parse"); return; }
                    // Leave TikTok's page (its scripts would redirect/reload over us) for a blank page of our
                    // own that still has the tiktok.com origin, so the CDN gets the session cookies + Referer.
                    ttFoundUrl = url; ttStage = 2;
                    notifyPage("dbg:url ok " + url.replaceAll("^https?://([^/]+).*$", "$1"));
                    tt.stopLoading();
                    // The player script is inlined into this document (our own, so no CSP), so it runs exactly
                    // when the document loads — no evaluateJavascript race with about:blank / the data load.
                    tt.loadDataWithBaseURL("https://www.tiktok.com/", ttPlayerHtml(url, ttPlayWhenReady), "text/html", "utf-8", null);
                } else if (r.startsWith("ERR")) {
                    ttFailDiag(r.substring(3).trim());
                } else if (android.os.SystemClock.uptimeMillis() >= ttDeadline) {
                    ttFailDiag("timeout");
                } else {
                    ui.postDelayed(this, TT_POLL_MS);
                }
            });
        }
    };

    // The player document: tv.html's TT_PLAYER_JS (a function (u, ap)) inlined and called with the H.264 URL.
    private String ttPlayerHtml(String url, boolean autoplay) {
        String call = ttPlayerJs + "(" + JSONObject.quote(url) + "," + autoplay + ");";
        return "<!doctype html><html><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"></head>"
             + "<body style=\"margin:0;background:#000;color:#8f8;font:12px monospace\">player document loaded, script pending…"
             + "<script>" + call.replace("</", "<\\/") + "</script></body></html>";
    }

    private void ttShow() {
        if (tt == null) return;
        ttVisible = true;
        tt.setVisibility(View.VISIBLE);
        web.setVisibility(View.INVISIBLE); // keep it laid out; it still receives the events we send
        tt.requestFocus();
        immersive();
        tt.evaluateJavascript("window.__tt&&__tt.play()", null);
        notifyPage("dbg:show");
        notifyPage("started");
    }

    private void ttClose() {
        ui.removeCallbacks(ttPoll);
        ttLoadingId = ttReadyId = null; ttStage = 0; ttFoundUrl = null;
        if (tt != null) {
            tt.evaluateJavascript("window.__tt&&__tt.stop()", null);
            tt.loadUrl("about:blank"); // drop the page (and its stream) entirely
            tt.setVisibility(View.GONE);
        }
        boolean was = ttVisible;
        ttVisible = false;
        web.setVisibility(View.VISIBLE);
        web.requestFocus();
        if (was) notifyPage("closed");
    }

    private void ttFail(String why) {
        ui.removeCallbacks(ttPoll);
        ttLoadingId = null;
        boolean wanted = ttPlayWhenReady;
        if (ttVisible) ttClose();
        if (wanted) notifyPage("error:" + why);
    }

    private void ttEvent(String ev) {
        notifyPage("dbg:ev " + ev);
        if ("ended".equals(ev)) notifyPage("ended");
        else if ("error".equals(ev)) { if (ttVisible) ttFail("playback"); }
        else if ("playing".equals(ev)) notifyPage("started");
    }

    private void notifyPage(String ev) {
        if (web != null) web.evaluateJavascript("window.tvTikTok&&tvTikTok(" + JSONObject.quote(ev) + ")", null);
    }

    // Remote while the TikTok player is showing. Returns true when the key was consumed.
    private boolean ttKey(KeyEvent ev) {
        String js = null; String page = null;
        switch (ev.getKeyCode()) {
            case KeyEvent.KEYCODE_DPAD_CENTER: case KeyEvent.KEYCODE_ENTER: case KeyEvent.KEYCODE_NUMPAD_ENTER:
            case KeyEvent.KEYCODE_MEDIA_PLAY_PAUSE: case KeyEvent.KEYCODE_MEDIA_PLAY: case KeyEvent.KEYCODE_MEDIA_PAUSE:
                js = "window.__tt&&__tt.toggle()"; break;
            case KeyEvent.KEYCODE_DPAD_LEFT: case KeyEvent.KEYCODE_MEDIA_REWIND: js = "window.__tt&&__tt.seek(-10)"; break;
            case KeyEvent.KEYCODE_DPAD_RIGHT: case KeyEvent.KEYCODE_MEDIA_FAST_FORWARD: js = "window.__tt&&__tt.seek(10)"; break;
            case KeyEvent.KEYCODE_DPAD_UP: page = "prev"; break;     // tv.html opens the neighbouring video
            case KeyEvent.KEYCODE_DPAD_DOWN: page = "next"; break;
            case KeyEvent.KEYCODE_BACK: case KeyEvent.KEYCODE_MEDIA_STOP: case KeyEvent.KEYCODE_ESCAPE:
                if (ev.getAction() == KeyEvent.ACTION_DOWN) ttClose();
                return true;
            default: return false; // volume etc. pass through
        }
        if (ev.getAction() == KeyEvent.ACTION_DOWN && tt != null) {
            if (js != null) tt.evaluateJavascript(js, null);
            if (page != null) notifyPage(page);
        }
        return true;
    }
}
