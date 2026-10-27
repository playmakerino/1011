package com.gathin.tvhome;

import android.content.ActivityNotFoundException;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.pm.ApplicationInfo;
import android.content.pm.PackageManager;
import android.content.pm.ResolveInfo;
import android.content.res.Resources;
import android.graphics.Outline;
import android.graphics.PixelFormat;
import android.graphics.drawable.Drawable;
import android.net.Uri;
import android.provider.Settings;
import android.util.DisplayMetrics;
import android.view.KeyEvent;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.ViewOutlineProvider;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * App tiles, YouTube style: a 16:9 banner with the app's name under it. The most opened apps come first
 * (LaunchCounts), then the rest by name.
 */
public class AppAdapter extends RecyclerView.Adapter<AppAdapter.Holder> {

    interface TileListener {
        void onTileFocused(int position, View card);

        /** Called for a D-pad direction key on a tile. Return true when handled (focus stays put). */
        boolean onTileVerticalKey(int position, int keyCode);

        /** Hold OK on a tile with tile_menu on: the activity shows the tile menu (remove from Home, app info). */
        void onTileLongPress(int position, View card);
    }

    static final class Entry {
        final String label;
        final ComponentName component;
        final String pkg;
        final Drawable banner;
        final Drawable icon;

        Entry(String label, ComponentName component, Drawable banner, Drawable icon) {
            this.label = label;
            this.component = component;
            this.pkg = component.getPackageName();
            this.banner = banner;
            this.icon = icon;
        }
    }

    /** Design size of a tile (dp), 16:9; tiles shrink from here to fit the columns and rows, see tileWidthPx. */
    static final float DESIGN_W_DP = 264f, DESIGN_H_DP = 148.5f;
    /** Gap between two tiles across, as between YouTube's thumbnails. */
    static final float GAP_DP = 18;
    /** item_app.xml in the grid: 8dp padding above and below, an 8dp gap and the 22dp name under the tile. */
    static final float ITEM_EXTRA_DP = 8 + 8 + 8 + 22;
    /** Room above the first row for the focus ring (MainActivity places the grid with it), and under the last. */
    static final float TOP_ROOM_DP = 12, BOTTOM_ROOM_DP = 16;
    /** The smallest share of the width-only tile size that fitting the rows into the height may go to. */
    static final float MIN_HEIGHT_FIT = 0.85f;
    /** Alpha of an unfocused tile's name: light grey, the focused one is white. */
    private static final float REST_NAME_ALPHA = 0.75f;

    /** Tile width for a grid of this inner width: the cell minus the gap, capped at the design size. */
    static int tileWidthPx(int innerWidthPx, int columns, float density) {
        int design = Math.round(DESIGN_W_DP * density);
        if (innerWidthPx <= 0 || columns <= 0) return design;
        int fit = (int) (innerWidthPx / columns - GAP_DP * density);
        return Math.max(Math.round(80 * density), Math.min(design, fit));
    }

    /**
     * Tile width that fits the columns across and, with rows > 1, that many rows down the grid's height; the smaller
     * wins. Before the grid has a height, only the width counts. The rows that still don't fit scroll.
     */
    static int tileWidthPx(int innerWidthPx, int gridHeightPx, int columns, int rows, float density) {
        int w = tileWidthPx(innerWidthPx, columns, density);
        if (gridHeightPx <= 0 || rows <= 1) return w;
        float perItem = (gridHeightPx - (TOP_ROOM_DP + BOTTOM_ROOM_DP) * density) / rows;
        int byHeight = Math.round((perItem - ITEM_EXTRA_DP * density) * DESIGN_W_DP / DESIGN_H_DP);
        return Math.max(Math.max(Math.round(80 * density), Math.round(w * MIN_HEIGHT_FIT)), Math.min(w, byHeight));
    }

    static int tileHeightPx(int tileWidthPx) {
        return Math.round(tileWidthPx * DESIGN_H_DP / DESIGN_W_DP);
    }

    /** Corner radius for a tile of this width: 12dp at the design width, proportionally less when smaller. */
    static float cornerRadius(int tileWidthPx, float density) {
        return 12f * density * Math.min(1f, tileWidthPx / (DESIGN_W_DP * density));
    }

    private final Context ctx;
    private final TileListener listener;
    private final int columns;
    /** Rows that must fit on the screen without scrolling (config.xml, rows). */
    private final int rows;
    /** Never shown as tiles (config.xml, hidden_apps), unless the owner ticks them in show/hide mode. */
    private final Set<String> hidden;
    /** Apps pre-seeded into the shown set (config.xml library_apps); empty by default. */
    private final Set<String> libraryPreload;
    /** Hold OK opens the activity's tile menu (config.xml, tile_menu); false opens App info. */
    private final boolean tileMenu;
    /** Packages with a leanback entry at the last reload(): their tiles launch with the leanback category. */
    private Set<String> leanbackPackages = new HashSet<>();
    /** Open counts the tiles were last sorted by (LaunchCounts), to tell when the order is out of date. */
    private Map<String, Integer> launchCounts = Collections.emptyMap();
    /** Show/hide mode (setChoosing): all apps listed, each with its check. */
    private boolean choosing;
    /** Packages that are on Home, as the show/hide mode ticks them. */
    private final Set<String> shownOnHome = new HashSet<>();
    private final List<Entry> items = new ArrayList<>();

    AppAdapter(Context ctx, TileListener listener, Config cfg) {
        this.ctx = ctx;
        this.listener = listener;
        this.columns = cfg.columns;
        this.rows = cfg.rows;
        this.hidden = new HashSet<>(cfg.hiddenApps);
        this.libraryPreload = new HashSet<>(cfg.libraryApps);
        this.tileMenu = cfg.tileMenu;
        // Tiles keep their identity across reload(), so a focused tile stays on its app instead of
        // its view being rebound to whatever app now sits in that slot.
        setHasStableIds(true);
    }

    /** Rebuilds the tiles: every app with a TV entry point, plus the ones ticked in show/hide mode. */
    void reload() {
        PackageManager pm = ctx.getPackageManager();
        List<ResolveInfo> found = new ArrayList<>(pm.queryIntentActivities(
                new Intent(Intent.ACTION_MAIN).addCategory(Intent.CATEGORY_LEANBACK_LAUNCHER), 0));
        Set<String> tvPackages = new HashSet<>();
        for (ResolveInfo ri : found) if (ri.activityInfo != null) tvPackages.add(ri.activityInfo.packageName);
        leanbackPackages = tvPackages;
        // Copy before merging: LibraryApps.load() may return an immutable empty set (#419).
        Set<String> added = new HashSet<>(LibraryApps.load(ctx));
        added.addAll(libraryPreload);
        Set<String> removed = LibraryApps.loadRemoved(ctx);
        if (!added.isEmpty() || choosing) {
            Set<String> seen = new HashSet<>(tvPackages);
            for (ResolveInfo ri : pm.queryIntentActivities(
                    new Intent(Intent.ACTION_MAIN).addCategory(Intent.CATEGORY_LAUNCHER), 0)) {
                // Show/hide mode lists the owner's own phone-style apps, not the firmware's system tools.
                boolean own = ri.activityInfo != null
                        && (ri.activityInfo.applicationInfo.flags & ApplicationInfo.FLAG_SYSTEM) == 0;
                if (ri.activityInfo != null && ((choosing && own) || added.contains(ri.activityInfo.packageName))
                        && seen.add(ri.activityInfo.packageName)) found.add(ri);
            }
        }
        List<Entry> fresh = new ArrayList<>();
        Set<String> visibleNow = new HashSet<>();
        // Some system apps declare two leanback entry points under one name (Sony's Timers & Clock on the
        // BRAVIA VU31), which would show as two identical tiles: keep the first per package and label.
        Set<String> seen = new HashSet<>();
        for (ResolveInfo ri : found) {
            if (ri.activityInfo == null) continue;
            String pkg = ri.activityInfo.packageName;
            boolean onHome = LibraryApps.visible(tvPackages.contains(pkg), hidden.contains(pkg), added.contains(pkg), removed.contains(pkg));
            // Home's own package shows only its Bài tập tile, not Home itself.
            boolean self = pkg.equals(ctx.getPackageName());
            if ((self && !ri.activityInfo.name.equals(BtvnActivity.class.getName()))
                    || !ri.activityInfo.exported || !(onHome || choosing)) continue;
            if (onHome) visibleNow.add(pkg);
            ComponentName component = new ComponentName(pkg, ri.activityInfo.name);
            // An app label with a bidi override or line separator must not redraw the tile name as something else.
            String label = cleanLabel(String.valueOf(ri.loadLabel(pm)), pkg);
            if (!seen.add(pkg + '\n' + label)) continue;
            Drawable banner = loadBanner(pm, ri);
            // The icon is only drawn when there is no banner, so a tile with a banner skips loading it.
            Drawable icon = banner == null ? ri.loadIcon(pm) : null;
            fresh.add(new Entry(label, component, banner, icon));
        }
        Map<String, Integer> opens = LaunchCounts.load(ctx);
        launchCounts = opens;
        Collections.sort(fresh, (a, b) -> {
            // Most opened apps first; apps opened equally often by name.
            int used = Integer.compare(LaunchCounts.of(opens, b.pkg), LaunchCounts.of(opens, a.pkg));
            if (used != 0) return used;
            return a.label.compareToIgnoreCase(b.label);
        });
        shownOnHome.clear();
        shownOnHome.addAll(visibleNow);
        items.clear();
        items.addAll(fresh);
        notifyDataSetChanged();
    }

    private Drawable loadBanner(PackageManager pm, ResolveInfo ri) {
        if (LiveClockBanner.PACKAGE.equals(ri.activityInfo.packageName)) return new LiveClockBanner(ctx);
        int id = ri.activityInfo.banner;
        if (id == 0) id = ri.activityInfo.applicationInfo.banner;
        Drawable banner = null;
        if (id != 0) {
            try {
                Resources resources = pm.getResourcesForApplication(ri.activityInfo.applicationInfo);
                // Keep at least xhdpi detail rather than downsampling the artwork.
                int density = Math.max(DisplayMetrics.DENSITY_XHIGH, ctx.getResources().getDisplayMetrics().densityDpi);
                banner = resources.getDrawableForDensity(id, density, null);
            } catch (PackageManager.NameNotFoundException | Resources.NotFoundException ignored) {
            }
        }
        if (banner == null) banner = ri.activityInfo.loadBanner(pm);
        // A square "banner" counts as none: the tile shows the app's icon and name instead of a blur.
        return banner != null && isBannerShaped(banner.getIntrinsicWidth(), banner.getIntrinsicHeight()) ? banner : null;
    }

    /**
     * An app's label as a tile shows it: control, format (bidi overrides, zero width joiners), line and paragraph
     * separator characters become spaces, runs of spaces collapse, at most 40 characters (never cutting a surrogate
     * pair), the fallback (package name) when nothing is left.
     */
    static String cleanLabel(String s, String fallback) {
        if (s == null) return fallback;
        StringBuilder b = new StringBuilder(Math.min(s.length(), 48));
        boolean space = true;   // leading spaces are dropped too
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            int type = Character.getType(c);
            boolean blank = c == ' ' || Character.isISOControl(c) || Character.isWhitespace(c) || type == Character.FORMAT
                    || type == Character.LINE_SEPARATOR || type == Character.PARAGRAPH_SEPARATOR
                    || type == Character.SPACE_SEPARATOR;
            if (blank) {
                if (!space) b.append(' ');
                space = true;
                continue;
            }
            boolean pair = Character.isHighSurrogate(c) && i + 1 < s.length() && Character.isLowSurrogate(s.charAt(i + 1));
            if (b.length() + (pair ? 2 : 1) > 40) break;
            b.append(c);
            if (pair) b.append(s.charAt(++i));
            space = false;
        }
        String out = b.toString().trim();
        return out.isEmpty() ? fallback : out;
    }

    /**
     * Some apps declare a small square image as their banner (Rockchip's Media Center ships a 64 px one). Cropped
     * over a 16:9 tile it is a blur. A drawable with no intrinsic size (a colour, a shape) still fills the tile.
     */
    static boolean isBannerShaped(int width, int height) {
        return width <= 0 || height <= 0 || width >= height * 1.4f;
    }

    /** Lets go of every tile and its artwork (Home is in the background and memory is short). */
    void clear() {
        items.clear();
        notifyDataSetChanged();
    }

    @NonNull
    @Override
    public Holder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View v = LayoutInflater.from(parent.getContext()).inflate(R.layout.item_app, parent, false);
        float density = parent.getResources().getDisplayMetrics().density;
        int width = parent.getWidth() > 0 ? parent.getWidth() : parent.getMeasuredWidth();
        int inner = width - parent.getPaddingLeft() - parent.getPaddingRight();
        int w = tileWidthPx(inner, parent.getHeight(), columns, rows, density), h = tileHeightPx(w);
        View card = v.findViewById(R.id.card);
        ViewGroup.LayoutParams cardLp = card.getLayoutParams();
        cardLp.width = w;
        cardLp.height = h;
        card.setLayoutParams(cardLp);
        View name = v.findViewById(R.id.name);
        ViewGroup.MarginLayoutParams nameLp = (ViewGroup.MarginLayoutParams) name.getLayoutParams();
        nameLp.width = w;
        nameLp.topMargin = h + Math.round(8 * density);
        name.setLayoutParams(nameLp);
        return new Holder(v, listener);
    }

    @Override
    public void onBindViewHolder(@NonNull Holder h, int position) {
        Entry e = items.get(position);
        h.name.setText(e.label);
        h.name.setAlpha(h.card.isFocused() ? 1f : REST_NAME_ALPHA);   // a rebind after reload() can hit the focused tile
        // A fully opaque banner covers the whole card (centerCrop), so the card's own fill under it is drawn for
        // nothing on every frame; keep it under banners with transparent parts and under icon tiles.
        h.card.setBackground(e.banner != null && e.banner.getOpacity() == PixelFormat.OPAQUE ? null : h.cardBackground);
        if (e.banner != null) {
            h.banner.setImageDrawable(e.banner);
            h.banner.setVisibility(View.VISIBLE);
            h.icon.setVisibility(View.GONE);
            h.label.setVisibility(View.GONE);
        } else {
            h.banner.setImageDrawable(null);
            h.banner.setVisibility(View.GONE);
            h.icon.setImageDrawable(e.icon);
            h.icon.setVisibility(View.VISIBLE);
            h.label.setText(e.label);
            h.label.setVisibility(View.VISIBLE);
        }
        boolean shown = shownOnHome.contains(e.pkg);
        h.check.setVisibility(choosing ? View.VISIBLE : View.GONE);
        h.check.setImageResource(shown ? R.drawable.yt_check_on : R.drawable.yt_check_off);
        h.card.setAlpha(choosing && !shown ? 0.4f : 1f);
        h.card.setOnClickListener(v -> launch(e));
        h.card.setOnLongClickListener(v -> {
            if (tileMenu) {
                int pos = h.getBindingAdapterPosition();
                if (pos != RecyclerView.NO_POSITION) listener.onTileLongPress(pos, v);
                return true;
            }
            Intent i = new Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS, Uri.parse("package:" + e.pkg));
            i.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            try {
                ctx.startActivity(i);
            } catch (ActivityNotFoundException ignored) {
            }
            return true;
        });
    }

    /** Opens the tile's activity by explicit component. */
    private void launch(Entry e) {
        Intent i = new Intent(Intent.ACTION_MAIN)
                .setComponent(e.component)
                .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_RESET_TASK_IF_NEEDED);
        // TV apps launch with the same leanback intent as from the stock launcher or the remote, so an app
        // already running resumes instead of restarting; only phone-style apps use plain MAIN.
        if (leanbackPackages.contains(e.pkg)) i.addCategory(Intent.CATEGORY_LEANBACK_LAUNCHER);
        try {
            ctx.startActivity(i);
        } catch (Exception ex) {
            Toast.makeText(ctx, ctx.getString(R.string.cant_open, e.label), Toast.LENGTH_SHORT).show();
        }
    }

    @Override
    public int getItemCount() {
        return items.size();
    }

    @Override
    public long getItemId(int position) {
        return items.get(position).component.flattenToShortString().hashCode();
    }

    /** True when an app was opened more often than one placed before it, so the tiles need sorting again. */
    boolean launchOrderStale() {
        Map<String, Integer> now = LaunchCounts.load(ctx);
        if (now.equals(launchCounts)) return false;
        int prev = Integer.MAX_VALUE;
        for (Entry e : items) {
            int n = LaunchCounts.of(now, e.pkg);
            if (n > prev) return true;
            prev = n;
        }
        launchCounts = now;
        return false;
    }

    /**
     * Show/hide mode: every installed app is a tile with a check (on Home) or an empty ring (hidden), and the
     * owner ticks them in place. Takes effect at the next reload().
     */
    void setChoosing(boolean on) {
        choosing = on;
    }

    boolean isChoosing() {
        return choosing;
    }

    /** Flips the tile's app between shown and hidden, saves it, and redraws the tile. False if it could not save. */
    boolean toggleShown(int position) {
        if (position < 0 || position >= items.size()) return false;
        String pkg = items.get(position).pkg;
        boolean show = !shownOnHome.contains(pkg);
        if (!LibraryApps.save(ctx, pkg, show)) return false;
        if (show) shownOnHome.add(pkg);
        else shownOnHome.remove(pkg);
        notifyItemChanged(position);
        return true;
    }

    /** Stable key for the app at a position (its component), or null. */
    String keyAt(int position) {
        return position >= 0 && position < items.size() ? items.get(position).component.flattenToShortString() : null;
    }

    /** Position of the app with this key, or -1 when it is gone. */
    int positionOf(String key) {
        if (key == null) return -1;
        for (int i = 0; i < items.size(); i++) {
            if (items.get(i).component.flattenToShortString().equals(key)) return i;
        }
        return -1;
    }

    String labelAt(int position) {
        return position >= 0 && position < items.size() ? items.get(position).label : "";
    }

    String packageAt(int position) {
        return position >= 0 && position < items.size() ? items.get(position).pkg : null;
    }

    static final class Holder extends RecyclerView.ViewHolder {
        final View card;
        /** item_app.xml's tile_bg: the dark card behind an icon tile, or behind a banner that has transparent parts. */
        final Drawable cardBackground;
        final ImageView banner;
        final ImageView icon;
        final TextView label;
        final TextView name;
        final ImageView check;

        Holder(View v, TileListener listener) {
            super(v);
            card = v.findViewById(R.id.card);
            cardBackground = card.getBackground();
            banner = v.findViewById(R.id.banner);
            icon = v.findViewById(R.id.icon);
            label = v.findViewById(R.id.label);
            name = v.findViewById(R.id.name);
            check = v.findViewById(R.id.check);

            final float density = v.getResources().getDisplayMetrics().density;
            card.setOutlineProvider(new ViewOutlineProvider() {
                @Override
                public void getOutline(View view, Outline outline) {
                    outline.setRoundRect(0, 0, view.getWidth(), view.getHeight(), cornerRadius(view.getWidth(), density));
                }
            });
            card.setClipToOutline(true);

            card.setOnKeyListener((view, keyCode, event) -> {
                if (event.getAction() != KeyEvent.ACTION_DOWN) return false;
                if (keyCode != KeyEvent.KEYCODE_DPAD_UP && keyCode != KeyEvent.KEYCODE_DPAD_DOWN
                        && keyCode != KeyEvent.KEYCODE_DPAD_LEFT && keyCode != KeyEvent.KEYCODE_DPAD_RIGHT) return false;
                int pos = getBindingAdapterPosition();
                return listener != null && pos != RecyclerView.NO_POSITION && listener.onTileVerticalKey(pos, keyCode);
            });

            // Like YouTube: the tile keeps its size and its name keeps its weight; only the name turns from grey to
            // white, at once, while the ring (MainActivity's FocusRing) jumps onto the tile.
            card.setOnFocusChangeListener((view, focused) -> {
                name.setAlpha(focused ? 1f : REST_NAME_ALPHA);
                int pos = getBindingAdapterPosition();
                if (focused && listener != null && pos != RecyclerView.NO_POSITION) {
                    listener.onTileFocused(pos, view);
                }
            });
        }
    }
}
