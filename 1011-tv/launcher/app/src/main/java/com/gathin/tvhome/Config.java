package com.gathin.tvhome;

import android.content.Context;
import android.content.res.Resources;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;

/** The launcher's settings, from res/values/config.xml. Change them there and rebuild. */
final class Config {

    /** Tiles per row. */
    final int columns;
    /** Rows of tiles that fit on the screen without scrolling; the tiles shrink for them. */
    final int rows;
    /** Never shown as tiles unless ticked in show/hide mode. */
    final List<String> hiddenApps;
    /** Shown on Home even without a TV entry point, as if ticked in show/hide mode. */
    final List<String> libraryApps;
    /** Hold OK on a tile opens a menu (Remove from Home, App info) instead of App info. */
    final boolean tileMenu;
    /** The tiles' entrance and the fades. */
    final boolean animations;
    /** Calmer motion for weak GPUs: short fades, no tile entrance. */
    final boolean reducedMotion;
    /** Minutes Home may sit untouched before the clock screensaver (ClockActivity); 0 is off. */
    final int homeIdleClockMinutes;

    private Config(Resources res) {
        columns = Math.max(1, res.getInteger(R.integer.columns));
        rows = Math.max(1, res.getInteger(R.integer.rows));
        hiddenApps = Collections.unmodifiableList(Arrays.asList(res.getStringArray(R.array.hidden_apps)));
        libraryApps = Collections.unmodifiableList(Arrays.asList(res.getStringArray(R.array.library_apps)));
        tileMenu = res.getBoolean(R.bool.tile_menu);
        animations = res.getBoolean(R.bool.animations);
        reducedMotion = res.getBoolean(R.bool.reduced_motion);
        homeIdleClockMinutes = Math.max(0, res.getInteger(R.integer.home_idle_clock_minutes));
    }

    static Config load(Context ctx) {
        return new Config(ctx.getResources());
    }
}
