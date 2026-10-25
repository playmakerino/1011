package com.gathin.tvhome;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.RectF;
import android.util.AttributeSet;
import android.view.View;

/**
 * The focus ring, YouTube style: a solid white border just outside the focused tile, with a small gap, so it shows
 * on white banners too. One instance floats over the grid; MainActivity puts it on the focused tile at once.
 * The view is the tile plus {@link #INSET_DP} on every side, which leaves room for the ring.
 */
public class FocusRing extends View {

    /** Room around the tile inside this view (MainActivity sizes the view with it). */
    static final float INSET_DP = 6f;
    private static final float GAP_DP = 1.5f, STROKE_DP = 3f;

    private final Paint ring = new Paint(Paint.ANTI_ALIAS_FLAG);
    private final RectF rect = new RectF();
    private final float density;
    private float radius;

    public FocusRing(Context context, AttributeSet attrs) {
        super(context, attrs);
        density = getResources().getDisplayMetrics().density;
        radius = 12f * density;
        ring.setStyle(Paint.Style.STROKE);
        ring.setStrokeWidth(STROKE_DP * density);
        ring.setColor(Color.WHITE);
        // Cache the ring as a texture: moving it only changes its translation.
        setLayerType(LAYER_TYPE_HARDWARE, null);
    }

    /** The tile's corner radius; the ring follows it, widened by its distance from the tile. */
    void setRadius(float px) {
        radius = px;
        invalidate();
    }

    @Override
    protected void onDraw(Canvas canvas) {
        float inset = INSET_DP * density;
        float out = (GAP_DP + STROKE_DP / 2f) * density;
        rect.set(inset - out, inset - out, getWidth() - inset + out, getHeight() - inset + out);
        canvas.drawRoundRect(rect, radius + out, radius + out, ring);
    }
}
