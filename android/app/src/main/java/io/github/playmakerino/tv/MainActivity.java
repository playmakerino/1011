package io.github.playmakerino.tv;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.graphics.Bitmap;
import android.graphics.Color;
import android.net.Uri;
import android.os.Bundle;
import android.view.Gravity;
import android.view.KeyEvent;
import android.view.View;
import android.view.ViewGroup;
import android.view.WindowManager;
import android.webkit.RenderProcessGoneDetail;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceError;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.TextView;

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

    @SuppressLint("SetJavaScriptEnabled")
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
        if (fullscreenView != null) {
            web.evaluateJavascript("document.exitFullscreen&&document.exitFullscreen()", null);
            return;
        }
        if (web.canGoBack()) { web.goBack(); return; } // tv.html keeps an entry for the open player, so Back closes it first
        super.onBackPressed();
    }

    @Override protected void onSaveInstanceState(Bundle out) { super.onSaveInstanceState(out); web.saveState(out); }
    @Override protected void onPause() { super.onPause(); web.onPause(); }
    @Override protected void onResume() { super.onResume(); web.onResume(); }
    @Override protected void onDestroy() { web.destroy(); super.onDestroy(); }
}
