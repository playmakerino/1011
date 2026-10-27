package com.gathin.tvhome;

import org.junit.Test;

import static org.junit.Assert.assertEquals;

public class LaunchCountsTest {
    private static final String SELF = "com.gathin.tvhome";
    private static final String HOME = SELF + ".MainActivity";
    private static final String BTVN = SELF + ".BtvnActivity";

    @Test
    public void otherAppsAreCountedByPackage() {
        assertEquals("com.google.android.youtube.tv",
                LaunchCounts.key(SELF, "com.google.android.youtube.tv", "com.google.android.apps.youtube.tv.activity.ShellActivity"));
    }

    @Test
    public void homeScreensAreCountedOneByOne() {
        assertEquals(SELF + "/" + BTVN, LaunchCounts.key(SELF, SELF, BTVN));
        assertEquals(SELF + "/" + HOME, LaunchCounts.key(SELF, SELF, HOME));
    }

    @Test
    public void baiTapGetsOnlyItsOwnOpens() {
        LaunchCounts.Tally t = new LaunchCounts.Tally(SELF);
        t.resumed(SELF, HOME);
        t.resumed(SELF, BTVN);
        t.resumed(SELF, HOME);
        t.resumed("com.google.android.youtube.tv", "Shell");
        t.resumed("com.google.android.youtube.tv", "Watch");   // another screen of the same app: not another open
        t.resumed(SELF, HOME);
        t.resumed(SELF, HOME);                                   // resumed again without leaving: not another open
        assertEquals(1, LaunchCounts.of(t.counts, LaunchCounts.key(SELF, SELF, BTVN)));
        assertEquals(1, LaunchCounts.of(t.counts, "com.google.android.youtube.tv"));
        assertEquals(3, LaunchCounts.of(t.counts, LaunchCounts.key(SELF, SELF, HOME)));
    }

    @Test
    public void eventsWithoutPackageAreSkipped() {
        LaunchCounts.Tally t = new LaunchCounts.Tally(SELF);
        t.resumed(null, null);
        assertEquals(0, t.counts.size());
    }
}
