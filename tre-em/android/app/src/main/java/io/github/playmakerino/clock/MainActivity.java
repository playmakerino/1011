package io.github.playmakerino.clock;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.graphics.Color;
import android.os.Bundle;
import android.view.Gravity;
import android.view.KeyEvent;
import android.view.View;
import android.view.WindowManager;
import android.webkit.WebResourceError;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.FrameLayout;
import android.widget.TextView;

/**
 * The kids' clock pages from GitHub Pages in a full-screen WebView: it opens on Đồng Hồ, and a two-segment switch at the top
 * right goes to Học Đồng Hồ and back.
 * The pages' tv-nav.js turns the remote's arrows and OK into focus moves and clicks; it only runs because of the
 * "TVApp/" tag added to the user agent.
 */
public class MainActivity extends Activity {

    private static final String URL = "https://playmakerino.github.io/1011/tre-em/dong-ho.html";
    private static final int BG = Color.BLACK;
    private WebView web;
    private TextView offline;

    @SuppressLint("SetJavaScriptEnabled")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        FrameLayout root = new FrameLayout(this);
        root.setBackgroundColor(BG);
        setContentView(root);

        web = new WebView(this);
        web.setBackgroundColor(BG);
        web.setFocusable(true);
        web.setFocusableInTouchMode(true);
        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);           // the pages keep stars and labels in localStorage
        s.setUseWideViewPort(true);
        s.setLoadWithOverviewMode(true);
        s.setSupportZoom(false);
        s.setTextZoom(100);                     // ignore the system font size so the layout stays as designed
        s.setUserAgentString(s.getUserAgentString() + " TVApp/1");
        web.setWebViewClient(new WebViewClient() {
            @Override
            public void onReceivedError(WebView view, WebResourceRequest request, WebResourceError error) {
                if (request.isForMainFrame()) offline.setVisibility(View.VISIBLE);
            }

            @Override
            public void onPageFinished(WebView view, String url) {
                web.requestFocus();
            }
        });
        root.addView(web, new FrameLayout.LayoutParams(-1, -1));

        offline = new TextView(this);
        offline.setText("Không vào được mạng. Bấm OK để thử lại.");
        offline.setTextSize(24);
        offline.setTextColor(0xFFF1F1F1);
        offline.setGravity(Gravity.CENTER);
        offline.setBackgroundColor(BG);
        offline.setVisibility(View.GONE);
        root.addView(offline, new FrameLayout.LayoutParams(-1, -1));

        immersive();
        if (savedInstanceState == null || web.restoreState(savedInstanceState) == null) web.loadUrl(URL);
        web.requestFocus();
    }

    private void immersive() {
        getWindow().getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_FULLSCREEN
                | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
                | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION);
    }

    @Override
    public void onWindowFocusChanged(boolean hasFocus) {
        super.onWindowFocusChanged(hasFocus);
        if (hasFocus) immersive();
    }

    @Override
    public boolean dispatchKeyEvent(KeyEvent event) {
        if (offline.getVisibility() == View.VISIBLE && event.getAction() == KeyEvent.ACTION_UP
                && (event.getKeyCode() == KeyEvent.KEYCODE_DPAD_CENTER || event.getKeyCode() == KeyEvent.KEYCODE_ENTER)) {
            offline.setVisibility(View.GONE);
            web.reload();
            return true;
        }
        return super.dispatchKeyEvent(event);
    }

    /**
     * Back closes what the page has open (TVNav.back); with nothing open, a clock page goes back to the menu,
     * and the menu leaves the app.
     */
    @Override
    public void onBackPressed() {
        if (offline.getVisibility() == View.VISIBLE) {
            super.onBackPressed();
            return;
        }
        web.evaluateJavascript("(window.TVNav && TVNav.back) ? TVNav.back() : false", result -> {
            if ("true".equals(result)) return;
            if (web.canGoBack()) web.goBack();
            else finish();
        });
    }

    @Override
    protected void onSaveInstanceState(Bundle outState) {
        super.onSaveInstanceState(outState);
        web.saveState(outState);
    }

    @Override
    protected void onDestroy() {
        web.destroy();
        super.onDestroy();
    }
}
