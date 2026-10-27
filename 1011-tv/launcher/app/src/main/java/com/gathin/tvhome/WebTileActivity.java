package com.gathin.tvhome;

import android.annotation.SuppressLint;
import android.app.Activity;
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
 * A tile that is a page of the 1011 site (https://playmakerino.github.io/1011/) in a full-screen WebView: each
 * subclass is its own leanback entry point, so AppAdapter lists it among the apps, and only names its page and
 * background. Every open loads the latest page. Back closes what the page has open (the pages' tv-nav.js, TVNav.back),
 * then goes back a page, then returns to Home.
 */
abstract class WebTileActivity extends Activity {

    private WebView web;
    private TextView offline;

    abstract String url();

    abstract int background();

    @SuppressLint("SetJavaScriptEnabled")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        int bg = background();
        FrameLayout root = new FrameLayout(this);
        root.setBackgroundColor(bg);
        setContentView(root);

        web = new WebView(this);
        web.setBackgroundColor(bg);
        web.setFocusable(true);
        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);           // the pages keep stars and labels in localStorage
        s.setUseWideViewPort(true);
        s.setLoadWithOverviewMode(true);
        s.setSupportZoom(false);
        s.setTextZoom(100);                     // ignore the system font size so the layout stays as designed
        // tv-nav.js turns the remote's arrows and OK into focus moves and clicks only under this tag.
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
        offline.setText(R.string.web_tile_offline);
        offline.setTextSize(24);
        boolean dark = (bg & 0xFF) < 0x80;
        offline.setTextColor(dark ? 0xFFF1F1F1 : 0xFF101010);
        offline.setGravity(Gravity.CENTER);
        offline.setBackgroundColor(bg);
        offline.setVisibility(View.GONE);
        root.addView(offline, new FrameLayout.LayoutParams(-1, -1));

        immersive();
        web.clearCache(true);
        web.loadUrl(url());
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

    @Override
    public void onBackPressed() {
        if (offline.getVisibility() == View.VISIBLE) {
            finish();
            return;
        }
        web.evaluateJavascript("(window.TVNav && TVNav.back) ? TVNav.back() : false", result -> {
            if ("true".equals(result)) return;
            if (web.canGoBack()) web.goBack();
            else finish();
        });
    }

    @Override
    protected void onDestroy() {
        web.destroy();
        super.onDestroy();
    }
}
