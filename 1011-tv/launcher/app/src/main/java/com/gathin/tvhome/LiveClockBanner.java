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
import java.util.Locale;

/**
 * The tile of "Đồng hồ" (DongHoActivity): the time as digits, hours and minutes (24 h), running, instead of a still
 * banner. Hours in the hour blue and minutes in the minute orange of the face on
 * https://playmakerino.github.io/1011/tre-em/dong-ho.html, with its pink between them as the colon.
 */
final class LiveClockBanner extends Drawable {

    private static final int BG = 0xFFFFFFFF;
    private static final int HOUR = 0xFF5A63D8;
    private static final int MINUTE = 0xFFF5921B;
    private static final int ACCENT = 0xFFFF5D97;

    private final Paint text = new Paint(Paint.ANTI_ALIAS_FLAG);
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
        Typeface b = ResourcesCompat.getFont(ctx, R.font.space_grotesk_700);
        text.setTypeface(b != null ? b : Typeface.DEFAULT_BOLD);
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
        c.drawColor(BG);

        now.setTimeInMillis(System.currentTimeMillis());
        String hh = String.format(Locale.ROOT, "%02d", now.get(Calendar.HOUR_OF_DAY));
        String mm = String.format(Locale.ROOT, "%02d", now.get(Calendar.MINUTE));

        // Text half the tile tall, at most 80% of its width; centred on the height of a digit.
        text.setTextSize(b.height() * 0.5f);
        float wh = text.measureText(hh), wc = text.measureText(":"), wm = text.measureText(mm);
        float scale = Math.min(1f, b.width() * 0.8f / (wh + wc + wm));
        text.setTextSize(text.getTextSize() * scale);
        wh *= scale;
        wc *= scale;
        wm *= scale;
        text.getTextBounds("0", 0, 1, digits);
        float x = b.exactCenterX() - (wh + wc + wm) / 2f;
        float y = b.exactCenterY() - digits.exactCenterY();

        text.setColor(HOUR);
        c.drawText(hh, x, y, text);
        text.setColor(ACCENT);
        c.drawText(":", x + wh, y, text);
        text.setColor(MINUTE);
        c.drawText(mm, x + wh + wc, y, text);

        if (running) {
            unscheduleSelf(tick);
            scheduleSelf(tick, SystemClock.uptimeMillis() + 60000 - System.currentTimeMillis() % 60000);
        }
    }

    /** Moves on at each new minute while the tile is on screen; the view hides it when Home leaves. */
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
