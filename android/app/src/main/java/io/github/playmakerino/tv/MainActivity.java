package io.github.playmakerino.tv;

import android.app.Activity;
import android.os.Bundle;
import android.view.KeyEvent;
import android.view.View;
import android.view.ViewGroup;
import android.view.WindowManager;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.FrameLayout;

public class MainActivity extends Activity {
    private static final String URL = "https://playmakerino.github.io/1011/tv.html";

    private WebView web;
    private FrameLayout root;
    private View fullscreenView;
    private WebChromeClient.CustomViewCallback fullscreenCallback;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);

        root = new FrameLayout(this);
        web = new WebView(this);
        root.addView(web, new FrameLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT));
        setContentView(root);

        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setMediaPlaybackRequiresUserGesture(false);
        s.setLoadWithOverviewMode(true);
        s.setUseWideViewPort(true);
        s.setSupportZoom(false);

        web.setWebViewClient(new WebViewClient());
        web.setWebChromeClient(new WebChromeClient() {
            @Override
            public void onShowCustomView(View view, CustomViewCallback callback) {
                if (fullscreenView != null) { callback.onCustomViewHidden(); return; }
                fullscreenView = view;
                fullscreenCallback = callback;
                web.setVisibility(View.GONE);
                root.addView(view, new FrameLayout.LayoutParams(
                        ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT));
                hideSystemUi(true);
            }

            @Override
            public void onHideCustomView() {
                if (fullscreenView == null) return;
                root.removeView(fullscreenView);
                fullscreenView = null;
                web.setVisibility(View.VISIBLE);
                hideSystemUi(false);
                if (fullscreenCallback != null) { fullscreenCallback.onCustomViewHidden(); fullscreenCallback = null; }
            }
        });

        if (savedInstanceState != null) web.restoreState(savedInstanceState); else web.loadUrl(URL);
    }

    private void hideSystemUi(boolean hide) {
        View d = getWindow().getDecorView();
        if (hide) {
            d.setSystemUiVisibility(View.SYSTEM_UI_FLAG_FULLSCREEN | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                    | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY | View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                    | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION);
        } else {
            d.setSystemUiVisibility(View.SYSTEM_UI_FLAG_VISIBLE);
        }
    }

    // Media buttons on TV remotes are not forwarded to the page as key events by WebView;
    // hand them to tv.html's window.tvKey(name) so seeking / play-pause works.
    @Override
    public boolean dispatchKeyEvent(KeyEvent ev) {
        if (ev.getAction() == KeyEvent.ACTION_DOWN) {
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
        if (web.canGoBack()) { web.goBack(); return; }
        super.onBackPressed();
    }

    @Override protected void onSaveInstanceState(Bundle out) { super.onSaveInstanceState(out); web.saveState(out); }
    @Override protected void onPause() { super.onPause(); web.onPause(); }
    @Override protected void onResume() { super.onResume(); web.onResume(); }
    @Override protected void onDestroy() { web.destroy(); super.onDestroy(); }
}
