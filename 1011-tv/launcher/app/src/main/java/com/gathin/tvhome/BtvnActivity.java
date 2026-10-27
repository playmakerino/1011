package com.gathin.tvhome;

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
 * The "Bài tập" tile: the homework page (btvn/index.html in the 1011 repo) in a full-screen WebView, read only
 * (?tv). Its own leanback entry point, so AppAdapter lists it as a tile next to the installed apps. Up and down
 * scroll a long message; Back returns to Home.
 */
public class BtvnActivity extends Activity {

    private static final String URL = "https://playmakerino.github.io/1011/btvn/?tv";
    private WebView web;
    private TextView offline;

    @SuppressLint("SetJavaScriptEnabled")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        FrameLayout root = new FrameLayout(this);
        root.setBackgroundColor(Color.WHITE);
        setContentView(root);

        web = new WebView(this);
        web.setBackgroundColor(Color.WHITE);
        web.setFocusable(true);
        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);           // Firebase keeps its connection state there
        s.setSupportZoom(false);
        s.setTextZoom(100);                     // the page sizes its text to the screen width
        web.setWebViewClient(new WebViewClient() {
            @Override
            public void onReceivedError(WebView view, WebResourceRequest request, WebResourceError error) {
                if (request.isForMainFrame()) offline.setVisibility(View.VISIBLE);
            }
        });
        root.addView(web, new FrameLayout.LayoutParams(-1, -1));

        offline = new TextView(this);
        offline.setText("Không vào được mạng. Bấm OK để thử lại.");
        offline.setTextSize(24);
        offline.setTextColor(0xFF101010);
        offline.setGravity(Gravity.CENTER);
        offline.setBackgroundColor(Color.WHITE);
        offline.setVisibility(View.GONE);
        root.addView(offline, new FrameLayout.LayoutParams(-1, -1));

        getWindow().getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_FULLSCREEN
                | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY);
        // Every open gets the latest page; the homework itself comes live from Firebase.
        web.clearCache(true);
        web.loadUrl(URL);
        web.requestFocus();
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
        finish();
    }

    @Override
    protected void onDestroy() {
        web.destroy();
        super.onDestroy();
    }
}
