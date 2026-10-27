package com.gathin.tvhome;

import android.app.usage.UsageEvents;
import android.app.usage.UsageStatsManager;
import android.content.Context;

import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

/**
 * How often each app was opened, from Android's usage statistics, so the grid can lead with the most used apps.
 *
 * Needs GET_USAGE_STATS, granted once over ADB: {@code appops set com.gathin.tvhome GET_USAGE_STATS allow}.
 * Without it the query returns nothing and every count is 0, so the grid keeps its usual order.
 */
final class LaunchCounts {

    private static final long WINDOW_MS = 30L * 24 * 60 * 60 * 1000;

    private LaunchCounts() {
    }

    /**
     * key -> times it came to the front in the last 30 days. Empty when the permission is missing. The key is the
     * package, except for Home's own screens (the Bài tập tile), see {@link #key}.
     */
    static Map<String, Integer> load(Context ctx) {
        UsageStatsManager usm = (UsageStatsManager) ctx.getSystemService(Context.USAGE_STATS_SERVICE);
        if (usm == null) return Collections.emptyMap();
        long now = System.currentTimeMillis();
        UsageEvents events;
        try {
            events = usm.queryEvents(now - WINDOW_MS, now);
        } catch (RuntimeException e) {
            return Collections.emptyMap();
        }
        if (events == null) return Collections.emptyMap();
        Tally tally = new Tally(ctx.getPackageName());
        UsageEvents.Event e = new UsageEvents.Event();
        while (events.hasNextEvent()) {
            events.getNextEvent(e);
            // MOVE_TO_FOREGROUND is ACTIVITY_RESUMED from Android 10 on (same value).
            if (e.getEventType() == UsageEvents.Event.MOVE_TO_FOREGROUND) tally.resumed(e.getPackageName(), e.getClassName());
        }
        return tally.counts;
    }

    /**
     * What an open is counted under: the package, so moving between screens inside one app is not another open.
     * Home's own package is the exception: Home itself and the Bài tập tile (BtvnActivity) are one package, and
     * Home comes to the front after every app, so its screens are counted one by one and the tile gets its own count.
     */
    static String key(String self, String pkg, String cls) {
        return pkg.equals(self) && cls != null ? pkg + '/' + cls : pkg;
    }

    /** Counts the opens in a run of resumed screens: only a change of key counts. */
    static final class Tally {
        final Map<String, Integer> counts = new HashMap<>();
        private final String self;
        private String front;

        Tally(String self) {
            this.self = self;
        }

        void resumed(String pkg, String cls) {
            if (pkg == null) return;
            String k = key(self, pkg, cls);
            if (k.equals(front)) return;
            front = k;
            Integer n = counts.get(k);
            counts.put(k, n == null ? 1 : n + 1);
        }
    }

    static int of(Map<String, Integer> counts, String key) {
        Integer n = counts.get(key);
        return n == null ? 0 : n;
    }
}
