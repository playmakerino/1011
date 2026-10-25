package com.gathin.tvhome;

import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.pm.ChangedPackages;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.graphics.Rect;
import android.graphics.drawable.ColorDrawable;
import android.net.ConnectivityManager;
import android.net.NetworkCapabilities;
import android.net.Uri;
import android.net.wifi.WifiInfo;
import android.net.wifi.WifiManager;
import android.os.Build;
import android.os.Bundle;
import android.provider.Settings;
import android.view.Gravity;
import android.view.KeyEvent;
import android.view.SoundEffectConstants;
import android.view.View;
import android.view.ViewGroup;
import android.view.animation.AnimationUtils;
import android.view.animation.DecelerateInterpolator;
import android.view.animation.LayoutAnimationController;
import android.widget.FrameLayout;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.PopupWindow;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.GridLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

/**
 * Home, YouTube style: a section title, a grid of 16:9 app tiles with their names under them, and one white
 * focus ring that jumps from tile to tile. A gear at the top right holds the network, show/hide and settings.
 */
public class MainActivity extends Activity implements AppAdapter.TileListener {

    /** Tiles per row (res/values/config.xml, columns). Set in onCreate. */
    static int COLUMNS = 4;
    private static final long MINUTE_MS = 60_000L;
    /** The longest any animation runs with reduced_motion on, in milliseconds. */
    private static final int REDUCED_MS = 90;

    private AppAdapter adapter;
    private RecyclerView grid;
    private FrameLayout root;
    private FocusRing ring;
    private View gear;
    private float density;
    private boolean animations;
    /** Calmer motion for weak GPUs (config.xml, reduced_motion): short fades, no tile entrance. */
    private boolean reducedMotion;
    /** Hold OK (or the remote's Menu key) on a tile opens the tile menu (config.xml, tile_menu). */
    private boolean tileMenuEnabled;
    /** Idle time on Home before ClockActivity; 0 is off (config.xml, home_idle_clock_minutes). */
    private long idleClockMs;
    private final Runnable showIdleClock = () -> startActivity(new Intent(this, ClockActivity.class));

    private int ringTileW;   // width of the tile the ring was last fitted to
    private boolean ringShown;
    private final Rect tileRect = new Rect();
    // Static so they survive the activity being destroyed while another app is open (low-memory TVs,
    // or Developer options, "Don't keep activities"); they only reset when the process dies.
    private static int lastFocused = 0;
    /** App of the last focused tile, so focus follows it when the app list changes. */
    private static String lastFocusedKey;

    /** Between onStop and onStart: Home was fully covered by an app. */
    private boolean stopped;
    /** Between onStart and onStop: Home is (at least partly) on screen. */
    private boolean started;
    /** Rebuild the tiles on the way back to Home only when apps changed meanwhile (TileRefresh). */
    private final TileRefresh tileRefresh = new TileRefresh();
    /** PackageManager's change counter at the last rebuild, to catch a package broadcast that never arrived. */
    private int packageSequence;
    /** The gear's or a tile's menu while one is open, so onPause can close it. */
    private PopupWindow openPopup;
    private RecyclerView.OnScrollListener pendingFocusScroll;

    private final IntentFilter packageFilter = new IntentFilter();
    private final BroadcastReceiver packageReceiver = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            // Updates send REMOVED followed by ADDED; keep the tile until the new APK is ready.
            if (Intent.ACTION_PACKAGE_REMOVED.equals(intent.getAction())
                    && intent.getBooleanExtra(Intent.EXTRA_REPLACING, false)) return;
            // In the background this only marks the tiles stale; onResume rebuilds them once.
            if (!tileRefresh.onPackagesChanged()) return;
            reloadApps(false);
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        density = getResources().getDisplayMetrics().density;
        Config cfg = Config.load(this);
        COLUMNS = cfg.columns;
        animations = cfg.animations;
        reducedMotion = cfg.reducedMotion;
        tileMenuEnabled = cfg.tileMenu;
        idleClockMs = cfg.homeIdleClockMinutes * MINUTE_MS;

        root = findViewById(R.id.root);
        // root fills the window with an opaque colour, so the window's own black under it is a second full-screen
        // fill on every frame for nothing. The starting window still uses the theme's background.
        getWindow().setBackgroundDrawable(null);
        ring = findViewById(R.id.ring);

        grid = findViewById(R.id.grid);
        grid.setLayoutManager(new GridLayoutManager(this, COLUMNS) {
            /**
             * Every "bring this tile on screen" scroll lands here, both RecyclerView's own on focus and
             * onTileFocused's: scroll just enough to show the rect between the grid's top edge and its bottom.
             */
            @Override
            public boolean requestChildRectangleOnScreen(@NonNull RecyclerView parent, @NonNull View child,
                                                         @NonNull Rect rect, boolean immediate,
                                                         boolean focusedChildVisible) {
                int top = child.getTop() + rect.top;
                int bottom = top + rect.height();
                // A row already fully on screen stays put, even inside the bottom padding. A row that has to
                // scroll in stops at the padding line, clear of the screen edge.
                int limitBottom = getHeight() - getPaddingBottom();
                int dy;
                if (top < 0) dy = top;
                else if (bottom <= getHeight()) dy = 0;
                else dy = Math.min(top, bottom - limitBottom);
                if (dy == 0) return false;
                if (immediate || reducedMotion || !animations) parent.scrollBy(0, dy);
                else parent.smoothScrollBy(0, dy);
                return true;
            }
        });
        grid.setHasFixedSize(true);
        grid.setItemAnimator(null);
        // Reduced motion: the tiles are simply there, with no entrance (reloadApps skips it there too).
        if (animations && !reducedMotion) {
            grid.setLayoutAnimation(new LayoutAnimationController(
                    AnimationUtils.loadAnimation(this, R.anim.tile_enter), 0.06f));
        }
        adapter = new AppAdapter(this, this, cfg);
        grid.setAdapter(adapter);

        // The grid starts under the section title, with room for the first row's focus ring.
        grid.addOnLayoutChangeListener((v, l, t, r, b, ol, ot, or, ob) -> {
            int want = (int) (AppAdapter.TOP_ROOM_DP * density);
            if (grid.getPaddingTop() != want) {
                grid.setPadding(grid.getPaddingLeft(), want, grid.getPaddingRight(), grid.getPaddingBottom());
            }
            // Cold start: the first focus can run before the grid has its final width or padding, leaving the
            // ring at the XML design size until a key is pressed.
            grid.post(this::refitRing);
        });

        // Keep the ring on its tile while the grid scrolls.
        grid.addOnScrollListener(new RecyclerView.OnScrollListener() {
            @Override
            public void onScrolled(@NonNull RecyclerView rv, int dx, int dy) {
                if (ringShown) ring.setTranslationY(ring.getTranslationY() - dy);
            }
        });

        gear = findViewById(R.id.btnSettings);
        gear.setOnClickListener(v -> showGearMenu());
        // The gear is the top bar's only button: Up and the sides go nowhere, Down goes back to the first-row tile
        // Up came from, not wherever the focus finder lands.
        gear.setOnKeyListener((v, keyCode, event) -> {
            if (event.getAction() != KeyEvent.ACTION_DOWN) return false;
            if (keyCode == KeyEvent.KEYCODE_DPAD_DOWN) {
                focusTile(lastFocused % COLUMNS);
                return true;
            }
            return keyCode == KeyEvent.KEYCODE_DPAD_UP || keyCode == KeyEvent.KEYCODE_DPAD_LEFT
                    || keyCode == KeyEvent.KEYCODE_DPAD_RIGHT;
        });

        // Hide the ring when focus leaves the tiles.
        getWindow().getDecorView().getViewTreeObserver().addOnGlobalFocusChangeListener((oldF, newF) -> {
            boolean onTile = newF != null && newF.getId() == R.id.card;
            if (!onTile) hideRing();
        });

        packageFilter.addAction(Intent.ACTION_PACKAGE_ADDED);
        packageFilter.addAction(Intent.ACTION_PACKAGE_REMOVED);
        packageFilter.addAction(Intent.ACTION_PACKAGE_CHANGED);
        packageFilter.addDataScheme("package");
        // Registered for the activity's whole life, not only while it is started: an app installed or updated while
        // another app is in front must still mark the tiles stale, or Home would have to rebuild on every return.
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            registerReceiver(packageReceiver, packageFilter, Context.RECEIVER_NOT_EXPORTED);
        } else {
            registerReceiver(packageReceiver, packageFilter);
        }
    }

    /**
     * Home pressed while Home is already in front: singleTask delivers it here, then onResume runs.
     * Back to the top with the first tile focused, like the stock launcher. Back from an app
     * never comes this way, so returning to the app you left from is unchanged.
     */
    @Override
    protected void onNewIntent(Intent intent) {
        super.onNewIntent(intent);
        if (intent == null || !intent.hasCategory(Intent.CATEGORY_HOME)) return;
        boolean wasChoosing = adapter.isChoosing();
        if (wasChoosing) adapter.setChoosing(false);
        grid.scrollToPosition(0);
        lastFocused = 0;
        lastFocusedKey = adapter.getItemCount() > 0 ? adapter.keyAt(0) : null;
        if (stopped) {
            tileRefresh.onHomeAgain();
        } else {
            // Still on screen: the tiles are current (unless show/hide mode was on), so only go back to the first
            // one; rebuilding would replay the entrance animation for nothing.
            if (wasChoosing) reloadTiles();
            grid.post(() -> focusTile(0));
        }
    }

    @Override
    protected void onStart() {
        super.onStart();
        stopped = false;
        started = true;
        tileRefresh.onStart();
    }

    @Override
    protected void onResume() {
        super.onResume();
        restartIdleClock();
        if (grid.getAdapter() == null) grid.setAdapter(adapter);   // dropped by onTrimMemory
        // An app opened more often than one before it moves up: rebuild as for a package change.
        switch (tileRefresh.onResume(packagesChangedSinceRebuild() || adapter.launchOrderStale())) {
            case REBUILD:
                reloadApps(true);
                break;
            case REFOCUS:
                // The same tiles: only the focus goes back, as after a rebuild, without replaying the entrance.
                reloadApps(true, false, false);
                break;
            default:
                break;
        }
    }

    /** Rebuilds the tiles, then puts focus back where it was. */
    private void reloadApps(boolean animate) {
        reloadApps(animate, true, true);
    }

    /**
     * @param rebuild  false keeps the tiles as they are and only puts focus back (TileRefresh.Action.REFOCUS).
     * @param entrance false puts focus back as an animated reload would, without replaying the tiles' entrance:
     *                 on a return to the same tiles it would only mark a change that didn't happen.
     */
    private void reloadApps(boolean animate, boolean rebuild, boolean entrance) {
        cancelPendingFocusScroll();
        // Capture the app before rebinding can move focus and overwrite its key.
        final String returnKey = lastFocusedKey;
        final int returnSlot = lastFocused;
        final boolean restoreFocus = animate || grid.hasFocus();
        if (restoreFocus) {
            ringShown = false;
            ring.setAlpha(0f);
        }
        if (rebuild) reloadTiles();
        if (animate && entrance && animations && !reducedMotion) {
            grid.scheduleLayoutAnimation();
            // A rebuild redraws the grid anyway; without one the entrance needs a draw to start.
            if (!rebuild) grid.invalidate();
        }
        if (restoreFocus) {
            // Return to the app we left from, or the same slot if that app is gone. Always refocus: after
            // reload() the view that holds focus may no longer show the app it had.
            grid.post(() -> {
                int pos = adapter.positionOf(returnKey);
                focusTile(pos >= 0 ? pos : returnSlot);
            });
        } else {
            // A package change must not steal focus from the gear or a menu.
            int pos = adapter.positionOf(returnKey);
            lastFocused = Math.max(0, Math.min(pos >= 0 ? pos : returnSlot, adapter.getItemCount() - 1));
            lastFocusedKey = adapter.keyAt(lastFocused);
        }
    }

    /** True when PackageManager reports apps changed since the last rebuild (one binder call). */
    private boolean packagesChangedSinceRebuild() {
        ChangedPackages changed = getPackageManager().getChangedPackages(packageSequence);
        return changed != null && !changed.getPackageNames().isEmpty();
    }

    private void reloadTiles() {
        // Read these before reload(): rebinding can move focus to the first tile and overwrite them.
        final String returnKey = lastFocusedKey;
        final int returnSlot = lastFocused;
        adapter.reload();
        lastFocusedKey = returnKey;
        lastFocused = returnSlot;
        ChangedPackages changed = getPackageManager().getChangedPackages(packageSequence);
        if (changed != null) packageSequence = changed.getSequenceNumber();
    }

    /** Any key on Home restarts the countdown to the idle clock. */
    @Override
    public void onUserInteraction() {
        super.onUserInteraction();
        restartIdleClock();
    }

    private void restartIdleClock() {
        root.removeCallbacks(showIdleClock);
        if (idleClockMs > 0) root.postDelayed(showIdleClock, idleClockMs);
    }

    @Override
    protected void onPause() {
        super.onPause();
        root.removeCallbacks(showIdleClock);
        cancelPendingFocusScroll();
        // Nothing of ours stays on screen over another app.
        if (openPopup != null) openPopup.dismiss();
    }

    @Override
    protected void onStop() {
        super.onStop();
        started = false;
        stopped = true;
        tileRefresh.onStop();
    }

    /**
     * Another app needs the memory while Home is in the background: let go of every tile's artwork, and
     * rebuild it when Home comes back. Not at UI_HIDDEN, the ordinary trip to an app, where keeping the
     * tiles is what makes the return instant.
     */
    @Override
    public void onTrimMemory(int level) {
        super.onTrimMemory(level);
        if (!MemoryTrimPolicy.shouldRelease(level, started)) return;
        adapter.clear();
        // Detach the adapter too: with Home stopped no layout pass runs, so the tile views (and the bitmaps
        // they hold) would stay attached until Home comes back. setAdapter(null) recycles them now.
        grid.setAdapter(null);
        grid.getRecycledViewPool().clear();
        tileRefresh.invalidate();
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        unregisterReceiver(packageReceiver);
    }

    // ---- keys ------------------------------------------------------------------------------------

    @Override
    public boolean dispatchKeyEvent(KeyEvent event) {
        if (tileMenuEnabled && openPopup == null && event.getKeyCode() == KeyEvent.KEYCODE_MENU) {
            int position = focusedTilePosition();
            if (position >= 0 && position < adapter.getItemCount()) {
                if (event.getAction() == KeyEvent.ACTION_UP && !event.isCanceled()) {
                    onTileLongPress(position, getCurrentFocus());
                }
                return true;
            }
        }
        if (adapter.isChoosing() && openPopup == null) return dispatchChoosing(event);
        return super.dispatchKeyEvent(event);
    }

    /** Adapter position of the focused tile, or -1 when focus is not on a tile. */
    private int focusedTilePosition() {
        View f = getCurrentFocus();
        if (f == null || f.getId() != R.id.card || !(f.getParent() instanceof View)) return -1;
        return grid.getChildAdapterPosition((View) f.getParent());
    }

    @Override
    public void onBackPressed() {
        // Home screen: Back goes nowhere.
    }

    // ---- show/hide mode --------------------------------------------------------------------------

    /** Show or hide apps (gear menu): every app on the grid with a check; OK ticks, Back finishes. */
    private void showAppVisibility() {
        adapter.setChoosing(true);
        reloadTiles();
        // After the rebuilt tiles are laid out, or the focus stays on the gear.
        grid.post(() -> focusTile(0));
        Toast.makeText(this, R.string.show_hide_hint, Toast.LENGTH_LONG).show();
    }

    /** Back in show/hide mode: the grid goes back to the apps that are ticked. */
    private void endAppVisibility() {
        adapter.setChoosing(false);
        reloadApps(false);
        grid.post(() -> focusTile(0));
    }

    /** Keys in show/hide mode: OK on a tile flips its check, Back ends the mode, arrows move as usual. */
    private boolean dispatchChoosing(KeyEvent event) {
        boolean down = event.getAction() == KeyEvent.ACTION_DOWN;
        int code = event.getKeyCode();
        boolean ok = code == KeyEvent.KEYCODE_DPAD_CENTER || code == KeyEvent.KEYCODE_ENTER
                || code == KeyEvent.KEYCODE_NUMPAD_ENTER;
        boolean back = code == KeyEvent.KEYCODE_BACK || code == KeyEvent.KEYCODE_ESCAPE;
        if (back) {
            if (!down) endAppVisibility();
            return true;
        }
        int pos = focusedTilePosition();
        if (ok && pos >= 0) {
            // Consumed on both edges, so the card never opens its app or its long-press menu here.
            if (!down && !event.isCanceled() && !adapter.toggleShown(pos)) {
                Toast.makeText(this, R.string.library_save_failed, Toast.LENGTH_LONG).show();
            }
            return true;
        }
        return super.dispatchKeyEvent(event);
    }

    // ---- focus ring ------------------------------------------------------------------------------

    @Override
    public void onTileFocused(int position, View card) {
        lastFocused = position;
        lastFocusedKey = adapter.keyAt(position);
        // Focus restored before the first layout (cold start): the tile has no size yet. Run again once it has.
        if (card.getWidth() == 0) {
            card.post(() -> {
                if (card.isFocused() && card.getWidth() > 0) onTileFocused(position, card);
            });
            return;
        }
        // The ring jumps onto the tile, as YouTube's focus does: no motion between tiles.
        Rect r = tileRect;
        r.set(0, 0, card.getWidth(), card.getHeight());
        root.offsetDescendantRectToMyCoords(card, r);
        float pad = FocusRing.INSET_DP * density;
        int w = (int) (card.getWidth() + 2 * pad);
        int h = (int) (card.getHeight() + 2 * pad);
        ViewGroup.LayoutParams lp = ring.getLayoutParams();
        if (lp.width != w || lp.height != h || card.getWidth() != ringTileW) {
            lp.width = w;
            lp.height = h;
            ring.setLayoutParams(lp);
            ring.setRadius(AppAdapter.cornerRadius(card.getWidth(), density));
        }
        ringTileW = card.getWidth();
        ring.setTranslationX(r.left - pad);
        ring.setTranslationY(r.top - pad);
        if (!ringShown) {
            ring.animate().cancel();
            ring.setAlpha(1f);
            ringShown = true;
        }
        // Scroll just enough so the whole ring (not only the tile) is visible.
        View item = (View) card.getParent();
        Rect reveal = new Rect(0, -(int) pad * 2, item.getWidth(), item.getHeight() + (int) pad);
        grid.requestChildRectangleOnScreen(item, reveal, reducedMotion);
    }

    /** Refits the ring to the focused holder once the grid layout and tile dimensions settle. */
    private void refitRing() {
        if (isDestroyed() || adapter.getItemCount() == 0) return;
        int pos = Math.max(0, Math.min(lastFocused, adapter.getItemCount() - 1));
        RecyclerView.ViewHolder vh = grid.findViewHolderForAdapterPosition(pos);
        View card = vh == null ? null : vh.itemView.findViewById(R.id.card);
        if (card == null || card.getWidth() <= 0 || !card.isFocused()) return;
        float pad = FocusRing.INSET_DP * density;
        int w = (int) (card.getWidth() + 2 * pad);
        int h = (int) (card.getHeight() + 2 * pad);
        if (!ringShown || card.getWidth() != ringTileW || ring.getWidth() != w || ring.getHeight() != h) {
            onTileFocused(pos, card);
        }
    }

    private void hideRing() {
        if (!ringShown) return;
        ringShown = false;
        ring.animate().cancel();
        if (animations && !reducedMotion) ring.animate().alpha(0f).setDuration(160).start();
        else ring.setAlpha(0f);
    }

    // ---- navigation ------------------------------------------------------------------------------

    @Override
    public boolean onTileVerticalKey(int position, int keyCode) {
        int count = adapter.getItemCount();
        int target;
        // Horizontal: swallow the key at a row's ends so focus never wraps to the next row or
        // escapes up into the top bar. Mid-row moves fall through to the default focus search.
        if (keyCode == KeyEvent.KEYCODE_DPAD_LEFT || keyCode == KeyEvent.KEYCODE_DPAD_RIGHT) {
            return GridNavigation.atHorizontalEdge(position, count, COLUMNS, false,
                    keyCode == KeyEvent.KEYCODE_DPAD_LEFT);
        }
        if (keyCode == KeyEvent.KEYCODE_DPAD_UP) {
            if (position < COLUMNS) return false;          // first row: let focus move to the gear
            target = position - COLUMNS;
        } else {
            int lastRowStart = ((count - 1) / COLUMNS) * COLUMNS;
            if (position >= lastRowStart) return true;
            target = Math.min(position + COLUMNS, count - 1);
        }
        focusTile(target);
        // The default focus search clicks for Left/Right; Up/Down are handled here, so click for them too.
        grid.playSoundEffect(keyCode == KeyEvent.KEYCODE_DPAD_UP
                ? SoundEffectConstants.NAVIGATION_UP : SoundEffectConstants.NAVIGATION_DOWN);
        return true;
    }

    private void cancelPendingFocusScroll() {
        if (pendingFocusScroll != null) {
            grid.removeOnScrollListener(pendingFocusScroll);
            pendingFocusScroll = null;
            grid.stopScroll();
        }
    }

    private void focusTile(int position) {
        cancelPendingFocusScroll();
        if (adapter.getItemCount() == 0) {
            gear.requestFocus();
            return;
        }
        final int pos = Math.max(0, Math.min(position, adapter.getItemCount() - 1));
        RecyclerView.ViewHolder vh = grid.findViewHolderForAdapterPosition(pos);
        if (vh != null) {
            View card = vh.itemView.findViewById(R.id.card);
            // Already focused (e.g. back from an app): no focus change fires, so restore the ring by hand.
            if (card.isFocused()) onTileFocused(pos, card);
            else card.requestFocus();
            return;
        }
        // Not laid out yet: scroll there, then focus once the scroll settles.
        if (!animations) {
            grid.scrollToPosition(pos);
            grid.post(() -> {
                RecyclerView.ViewHolder h = grid.findViewHolderForAdapterPosition(pos);
                if (h != null) h.itemView.findViewById(R.id.card).requestFocus();
            });
            return;
        }
        pendingFocusScroll = new RecyclerView.OnScrollListener() {
            @Override
            public void onScrollStateChanged(@NonNull RecyclerView rv, int newState) {
                if (newState != RecyclerView.SCROLL_STATE_IDLE) return;
                rv.removeOnScrollListener(this);
                if (pendingFocusScroll != this) return;
                pendingFocusScroll = null;
                RecyclerView.ViewHolder h = rv.findViewHolderForAdapterPosition(pos);
                View target = h != null ? h.itemView.findViewById(R.id.card) : rv.getChildAt(0);
                if (target != null) target.requestFocus();
            }
        };
        grid.addOnScrollListener(pendingFocusScroll);
        grid.smoothScrollToPosition(pos);
    }

    // ---- menus -----------------------------------------------------------------------------------

    /** The gear's menu: the network (with its name), Show or hide apps, and the TV's Settings. */
    private void showGearMenu() {
        View panel = getLayoutInflater().inflate(R.layout.popup_menu, root, false);
        LinearLayout rows = panel.findViewById(R.id.rows);
        PopupWindow popup = menuPopup(panel, (int) (220 * density));
        NetworkRow network = currentNetwork();
        addMenuRow(rows, popup, network.icon, getString(R.string.quick_network), network.name,
                () -> open(new Intent(Settings.ACTION_WIFI_SETTINGS)));
        addMenuRow(rows, popup, R.drawable.ic_apps, getString(R.string.show_hide_apps), null, this::showAppVisibility);
        addMenuRow(rows, popup, R.drawable.ic_settings, getString(R.string.settings), null,
                () -> open(new Intent(Settings.ACTION_SETTINGS)));
        panel.measure(View.MeasureSpec.UNSPECIFIED, View.MeasureSpec.UNSPECIFIED);
        popup.setWidth(Math.max((int) (220 * density), Math.min(panel.getMeasuredWidth(), (int) (360 * density))));
        dropIn(popup, panel, gear, Gravity.END);
        rows.getChildAt(0).requestFocus();
    }

    /**
     * Hold OK on a tile (tile_menu): a menu next to it. Remove from Home hides the app (Show or hide apps brings it
     * back); App info opens the TV's page for the app.
     */
    @Override
    public void onTileLongPress(int position, View card) {
        String pkg = adapter.packageAt(position);
        if (pkg == null || pkg.equals(getPackageName())) return;
        View panel = getLayoutInflater().inflate(R.layout.popup_menu, root, false);
        LinearLayout rows = panel.findViewById(R.id.rows);
        PopupWindow popup = menuPopup(panel, (int) (200 * density));
        addMenuRow(rows, popup, 0, getString(R.string.library_remove_shortcut), null, () -> {
            if (LibraryApps.save(this, pkg, false)) reloadApps(false);
            else Toast.makeText(this, R.string.library_save_failed, Toast.LENGTH_LONG).show();
        });
        // Some firmware has no App info page at all; a row that only toasts "can't open" helps nobody.
        Intent info = new Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS, Uri.parse("package:" + pkg));
        if (getPackageManager().resolveActivity(info, PackageManager.MATCH_DEFAULT_ONLY) == null) info = null;
        final Intent appInfo = info;
        if (appInfo != null) addMenuRow(rows, popup, 0, getString(R.string.library_app_info), null, () -> open(appInfo));
        panel.measure(View.MeasureSpec.UNSPECIFIED, View.MeasureSpec.UNSPECIFIED);
        popup.setWidth(Math.max((int) (200 * density), panel.getMeasuredWidth()));
        // Tiles near the bottom of the screen: open the menu above the tile when it would not fit below.
        int[] at = new int[2];
        card.getLocationInWindow(at);
        int gap = (int) (10 * density), height = panel.getMeasuredHeight();
        if (at[1] + card.getHeight() + gap + height <= root.getHeight()) {
            dropIn(popup, panel, card, Gravity.START);
        } else {
            panel.setAlpha(0f);
            panel.setPivotY(height);
            panel.setScaleY(0.92f);
            panel.setTranslationY(8 * density);
            popup.showAtLocation(root, Gravity.NO_GRAVITY, at[0], Math.max(0, at[1] - gap - height));
            panel.animate().alpha(1f).scaleY(1f).translationY(0f).setDuration(reducedMotion ? REDUCED_MS : 220)
                    .setInterpolator(new DecelerateInterpolator(1.6f)).start();
        }
        rows.getChildAt(0).requestFocus();
    }

    private PopupWindow menuPopup(View panel, int width) {
        final PopupWindow popup = new PopupWindow(panel, width, ViewGroup.LayoutParams.WRAP_CONTENT, true);
        popup.setBackgroundDrawable(new ColorDrawable(Color.TRANSPARENT));   // needed for Back to dismiss
        popup.setOutsideTouchable(true);
        popup.setAnimationStyle(0);
        popup.setElevation(0f);
        popup.setOnDismissListener(() -> {
            if (openPopup == popup) openPopup = null;
        });
        openPopup = popup;
        return popup;
    }

    /** Drop in: fade and unfold from the top edge, hanging under the anchor. */
    private void dropIn(PopupWindow popup, View panel, View anchor, int gravity) {
        panel.setAlpha(0f);
        panel.setPivotY(0f);
        panel.setScaleY(0.92f);
        panel.setTranslationY(-8 * density);
        popup.showAsDropDown(anchor, 0, (int) (10 * density), gravity);
        panel.animate().alpha(1f).scaleY(1f).translationY(0f).setDuration(reducedMotion ? REDUCED_MS : 220)
                .setInterpolator(new DecelerateInterpolator(1.6f)).start();
    }

    /** One menu row: an icon (0 for none), its title and an optional dim status on the right. */
    private void addMenuRow(LinearLayout rows, PopupWindow popup, int iconRes, String title, String status,
                            Runnable action) {
        View row = getLayoutInflater().inflate(R.layout.item_menu_row, rows, false);
        ImageView icon = row.findViewById(R.id.icon);
        if (iconRes != 0) icon.setImageResource(iconRes);
        else icon.setVisibility(View.GONE);
        ((TextView) row.findViewById(R.id.title)).setText(title);
        TextView statusView = row.findViewById(R.id.status);
        if (status != null && !status.isEmpty()) statusView.setText(status);
        else statusView.setVisibility(View.GONE);
        row.setOnClickListener(v -> {
            popup.dismiss();
            action.run();
        });
        // The OK-up after holding OK to open a tile's menu must not activate its first row.
        final boolean[] pressed = {false};
        row.setOnKeyListener((v, code, event) -> {
            if (code != KeyEvent.KEYCODE_DPAD_CENTER && code != KeyEvent.KEYCODE_ENTER) return false;
            if (event.getAction() == KeyEvent.ACTION_DOWN) {
                if (event.getRepeatCount() == 0) pressed[0] = true;
                return true;
            }
            boolean activate = pressed[0];
            pressed[0] = false;
            if (activate) {
                popup.dismiss();
                action.run();
            }
            return true;
        });
        rows.addView(row);
    }

    /** The network row's icon and the name it shows: the Wi-Fi network, Ethernet, or Offline. */
    private static final class NetworkRow {
        final int icon;
        final String name;

        NetworkRow(int icon, String name) {
            this.icon = icon;
            this.name = name;
        }
    }

    /** Reads the connection when the gear's menu opens (a few binder calls, only then). */
    private NetworkRow currentNetwork() {
        try {
            ConnectivityManager cm = getSystemService(ConnectivityManager.class);
            boolean wifi = false, ethernet = false, online = false;
            for (android.net.Network net : cm != null ? cm.getAllNetworks() : new android.net.Network[0]) {
                NetworkCapabilities caps = cm.getNetworkCapabilities(net);
                if (caps == null || caps.hasTransport(NetworkCapabilities.TRANSPORT_VPN)
                        || !caps.hasCapability(NetworkCapabilities.NET_CAPABILITY_INTERNET)) continue;
                online = true;
                if (caps.hasTransport(NetworkCapabilities.TRANSPORT_ETHERNET)) ethernet = true;
                if (caps.hasTransport(NetworkCapabilities.TRANSPORT_WIFI)) wifi = true;
            }
            if (!online) return new NetworkRow(R.drawable.ic_wifi, getString(R.string.offline));
            if (ethernet) return new NetworkRow(R.drawable.ic_ethernet, getString(R.string.ethernet));
            if (wifi) {
                WifiManager wm = (WifiManager) getApplicationContext().getSystemService(Context.WIFI_SERVICE);
                WifiInfo info = wm != null ? wm.getConnectionInfo() : null;
                String ssid = info != null ? info.getSSID() : null;
                if (ssid != null) {
                    ssid = ssid.replace("\"", "").trim();
                    if (!ssid.isEmpty() && !ssid.contains("unknown") && !ssid.equals("0x")) {
                        return new NetworkRow(R.drawable.ic_wifi, ssid);
                    }
                }
            }
        } catch (RuntimeException ignored) {
        }
        return new NetworkRow(R.drawable.ic_wifi, getString(R.string.wifi));
    }

    private void open(Intent i) {
        i.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        try {
            startActivity(i);
        } catch (ActivityNotFoundException | SecurityException e) {
            Toast.makeText(this, R.string.not_available, Toast.LENGTH_SHORT).show();
        }
    }
}
