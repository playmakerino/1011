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

    /** package -> times it came to the front in the last 30 days. Empty when the permission is missing. */
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
        Map<String, Integer> counts = new HashMap<>();
        UsageEvents.Event e = new UsageEvents.Event();
        String front = null;
        while (events.hasNextEvent()) {
            events.getNextEvent(e);
            // MOVE_TO_FOREGROUND is ACTIVITY_RESUMED from Android 10 on (same value). Only a change of app counts,
            // so moving between screens inside one app is not another open.
            if (e.getEventType() != UsageEvents.Event.MOVE_TO_FOREGROUND) continue;
            String pkg = e.getPackageName();
            if (pkg == null || pkg.equals(front)) continue;
            front = pkg;
            Integer n = counts.get(pkg);
            counts.put(pkg, n == null ? 1 : n + 1);
        }
        return counts;
    }

    static int of(Map<String, Integer> counts, String pkg) {
        Integer n = counts.get(pkg);
        return n == null ? 0 : n;
    }
}
