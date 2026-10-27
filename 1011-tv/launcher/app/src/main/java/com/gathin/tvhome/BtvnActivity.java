package com.gathin.tvhome;

import android.graphics.Color;

/** The "Bài tập" tile: the homework page (btvn/ in the 1011 repo), read only (?tv). Up and down scroll a long message. */
public class BtvnActivity extends WebTileActivity {

    @Override
    String url() {
        return "https://playmakerino.github.io/1011/btvn/?tv";
    }

    @Override
    int background() {
        return Color.WHITE;
    }
}
