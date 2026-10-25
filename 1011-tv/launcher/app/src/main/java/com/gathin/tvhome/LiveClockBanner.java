package com.gathin.tvhome;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.ColorFilter;
import android.graphics.Paint;
import android.graphics.PixelFormat;
import android.graphics.Rect;
import android.graphics.Typeface;
import android.graphics.drawable.Drawable;
import android.os.SystemClock;

import androidx.annotation.NonNull;
import androidx.core.content.res.ResourcesCompat;

import java.util.Calendar;

/**
 * The tile of the "Đồng Hồ" app (tre-em/android in the 1011 repo): its analog clock face, running, instead of the
 * app's still banner. Drawn like the face on https://playmakerino.github.io/1011/tre-em/dong-ho.html (white face,
 * hour ticks and numerals in the hour blue, minute ticks in orange, pink second hand), without the rings around it.
 * Every size below is the page's pixel size divided by its face radius (118 px), so the two keep the same shape.
 */
final class LiveClockBanner extends Drawable {

    static final String PACKAGE = "io.github.playmakerino.clock";

    private static final int BG = 0xFFFDF6F0;
    private static final int RIM = 0xFF2B2B2B;
    private static final int HOUR = 0xFF5A63D8;
    private static final int MINUTE = 0xFFF5921B;
    private static final int SECOND = 0xFFFF5D97;

    private final Paint paint = new Paint(Paint.ANTI_ALIAS_FLAG);
    private final Paint text = new Paint(Paint.ANTI_ALIAS_FLAG);
    private final Typeface regular;
    private final Typeface bold;
    private final Calendar now = Calendar.getInstance();
    private final Rect digits = new Rect();
    private boolean running;

    private final Runnable tick = new Runnable() {
        @Override
        public void run() {
            invalidateSelf();
        }
    };

    LiveClockBanner(Context ctx) {
        Typeface r = ResourcesCompat.getFont(ctx, R.font.space_grotesk_400);
        Typeface b = ResourcesCompat.getFont(ctx, R.font.space_grotesk_700);
        regular = r != null ? r : Typeface.DEFAULT;
        bold = b != null ? b : Typeface.DEFAULT_BOLD;
        text.setColor(HOUR);
        text.setTextAlign(Paint.Align.CENTER);
    }

    @Override
    public int getIntrinsicWidth() {
        return 640;
    }

    @Override
    public int getIntrinsicHeight() {
        return 360;
    }

    @Override
    public void draw(@NonNull Canvas c) {
        Rect b = getBounds();
        float cx = b.exactCenterX(), cy = b.exactCenterY();
        float r = b.height() * 0.46f;
        c.drawColor(BG);

        paint.setStyle(Paint.Style.FILL);
        paint.setColor(0xFFFFFFFF);
        c.drawCircle(cx, cy, r, paint);
        paint.setStyle(Paint.Style.STROKE);
        paint.setStrokeWidth(r / 118f);
        paint.setColor(RIM);
        c.drawCircle(cx, cy, r, paint);

        // Ticks: 5 px in from the rim, hour ticks 8 px long, minute ticks 4 px.
        float outer = r - r * 5 / 118f, inner = outer - r * 8 / 118f;
        paint.setStrokeCap(Paint.Cap.BUTT);
        for (int i = 0; i < 60; i++) {
            boolean major = i % 5 == 0;
            double a = Math.toRadians(i * 6);
            float sx = (float) Math.sin(a), sy = (float) -Math.cos(a);
            float len = r * (major ? 8 : 4) / 118f;
            paint.setColor(major ? HOUR : MINUTE);
            paint.setStrokeWidth(r * (major ? 1.5f : 1f) / 118f);
            c.drawLine(cx + sx * outer, cy + sy * outer, cx + sx * (outer - len), cy + sy * (outer - len), paint);
        }

        now.setTimeInMillis(System.currentTimeMillis());
        int h = now.get(Calendar.HOUR), m = now.get(Calendar.MINUTE), s = now.get(Calendar.SECOND);

        // Numerals 2 px inside the hour ticks; the current hour in bold, as on the page.
        float size = r * 15.2f / 118f;
        text.setTextSize(size);
        for (int n = 1; n <= 12; n++) {
            text.setTypeface(n % 12 == h ? bold : regular);
            String label = String.valueOf(n);
            text.getTextBounds(label, 0, label.length(), digits);
            double a = Math.toRadians(n * 30);
            float ux = (float) Math.sin(a), uy = (float) -Math.cos(a);
            float reach = Math.abs(ux) * digits.width() / 2f + Math.abs(uy) * digits.height() / 2f;
            float d = inner - r * 2 / 118f - reach;
            c.drawText(label, cx + ux * d, cy + uy * d - digits.exactCenterY(), text);
        }

        paint.setStrokeCap(Paint.Cap.ROUND);
        hand(c, cx, cy, (h + m / 60f + s / 3600f) * 30, r * 0.34f, r * 5 / 118f, HOUR);
        hand(c, cx, cy, (m + s / 60f) * 6, r * 0.55f, r * 3 / 118f, MINUTE);
        hand(c, cx, cy, s * 6, r * 0.62f, r * 1.5f / 118f, SECOND);

        // Pink hub with a 4 px white ring.
        paint.setStyle(Paint.Style.FILL);
        paint.setColor(0xFFFFFFFF);
        c.drawCircle(cx, cy, r * 8.5f / 118f, paint);
        paint.setColor(SECOND);
        c.drawCircle(cx, cy, r * 4.5f / 118f, paint);

        if (running) {
            unscheduleSelf(tick);
            scheduleSelf(tick, SystemClock.uptimeMillis() + 1000 - System.currentTimeMillis() % 1000);
        }
    }

    private void hand(Canvas c, float cx, float cy, float deg, float len, float width, int color) {
        double a = Math.toRadians(deg);
        paint.setStyle(Paint.Style.STROKE);
        paint.setStrokeWidth(width);
        paint.setColor(color);
        c.drawLine(cx, cy, cx + (float) Math.sin(a) * len, cy - (float) Math.cos(a) * len, paint);
    }

    /** Ticks once a second while the tile is on screen; the view hides it when Home leaves. */
    @Override
    public boolean setVisible(boolean visible, boolean restart) {
        boolean changed = super.setVisible(visible, restart);
        running = visible;
        if (visible) invalidateSelf();
        else unscheduleSelf(tick);
        return changed;
    }

    @Override
    public void setAlpha(int alpha) {
    }

    @Override
    public void setColorFilter(ColorFilter cf) {
    }

    @Override
    public int getOpacity() {
        return PixelFormat.OPAQUE;
    }
}
