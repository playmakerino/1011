package com.gathin.tvhome;

import org.junit.Test;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

/** AppAdapter.tileWidthPx with rows: that many rows of tiles must fit the grid's height without scrolling. */
public class TileFitTest {

    private static final float D = 2f;              // 1080p TV: 2 px per dp
    private static final int INNER = 1676;          // grid width minus padding at 1920 px
    private static final int GRID_H = 960;          // grid height under the section title at 1080 px

    private static int height(int tileW, int rows) {
        int itemH = AppAdapter.tileHeightPx(tileW) + Math.round(AppAdapter.ITEM_EXTRA_DP * D);
        return itemH * rows + Math.round((AppAdapter.TOP_ROOM_DP + AppAdapter.BOTTOM_ROOM_DP) * D);
    }

    @Test
    public void oneRowOrNoHeightKeepsTheWidthOnlySize() {
        int widthOnly = AppAdapter.tileWidthPx(INNER, 4, D);
        assertEquals(widthOnly, AppAdapter.tileWidthPx(INNER, GRID_H, 4, 1, D));
        assertEquals(widthOnly, AppAdapter.tileWidthPx(INNER, 0, 4, 3, D));   // not laid out yet
    }

    @Test
    public void threeRowsOfFourFitA1080pScreen() {
        int w = AppAdapter.tileWidthPx(INNER, GRID_H, 4, 3, D);
        assertTrue(w <= AppAdapter.tileWidthPx(INNER, 4, D));
        assertTrue("three rows fit", height(w, 3) <= GRID_H + 2);
    }

    @Test
    public void moreRowsStopAtTheFloorInsteadOfShrinkingTheTiles() {
        // Six rows would need tiles under half their size: they stop at 85% and the extra rows scroll instead.
        int floor = Math.round(AppAdapter.tileWidthPx(INNER, 4, D) * AppAdapter.MIN_HEIGHT_FIT);
        assertEquals(floor, AppAdapter.tileWidthPx(INNER, GRID_H, 4, 6, D));
    }

    @Test
    public void tilesStay16by9AndLeaveTheGap() {
        int w = AppAdapter.tileWidthPx(INNER, 4, D);
        assertEquals(Math.round(w * 9f / 16f), AppAdapter.tileHeightPx(w), 1);
        assertTrue("an 18dp gap per column", w * 4 + 4 * AppAdapter.GAP_DP * D <= INNER);
    }
}
