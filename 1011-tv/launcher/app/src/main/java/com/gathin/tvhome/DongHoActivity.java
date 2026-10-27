package com.gathin.tvhome;

import android.graphics.Color;

/**
 * The "Đồng hồ" tile: the kids' clock (tre-em/dong-ho.html in the 1011 repo); a switch at the top centre goes to Học
 * Đồng Hồ and back. Its tile is the running clock (LiveClockBanner). Until 10/2026 this was its own app
 * (io.github.playmakerino.clock, tre-em/android).
 */
public class DongHoActivity extends WebTileActivity {

    @Override
    String url() {
        return "https://playmakerino.github.io/1011/tre-em/dong-ho.html";
    }

    @Override
    int background() {
        return Color.BLACK;
    }
}
