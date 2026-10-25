/* Remote (D-pad) control for the kids' pages, used only inside the "Đồng Hồ" TV app (tre-em/android), which
 * adds "TVApp/" to the user agent. In a browser only the page switch (TVNav.pages) is added, nothing else.
 *
 * - Arrow keys move the focus between focusable elements (buttons, inputs, and anything with a tabindex), only
 *   inside an open popup when the page lists one in TVNav.scopes. Left / Right step through a group (elements
 *   with the same parent) in page order; elsewhere the focus goes to the nearest element wholly on that side,
 *   on the same row for Left / Right.
 * - OK (Enter) presses the focused element; buttons do that by themselves, other elements get a click().
 * - The app's Back key calls TVNav.back(): the page's TVNav.onBack() closes what is open and returns true;
 *   false lets the app go back to the TV's home screen.
 *
 * - TVNav.pages adds a small switch at the top centre (on TV, computer and phone), drawn like the Chat / Code
 *   switch of the Claude desktop app: a soft grey track, the current page on a raised white segment. The other
 *   segment opens its page in place of this one, so the app's history stays one page deep and Back always
 *   leaves the app.
 *
 * A page sets window.TVNav = { scopes: [...popup selectors...], onBack: function(){...}, first: 'selector',
 * pages: [{ href: 'page.html', label: 'Name' }, ...] } before loading this file. */
(function () {
  var cfg = window.TVNav = window.TVNav || {};
  var tv = /TVApp\//.test(navigator.userAgent);

  var css = document.createElement('style');
  // The focus ring is its own element (.tv-ring, below) on top of everything: an outline is painted with its
  // element, so a neighbour drawn later or a higher layer covers it.
  css.textContent = '.tv-nav :focus{outline:none !important}' +
    '.tv-ring{position:fixed;z-index:2147483647;pointer-events:none;box-sizing:border-box;' +
    'border:3px solid #2b2b33;display:none}' +
    '.tv-seg{position:fixed;top:14px;left:50%;transform:translateX(-50%);z-index:50;display:flex;gap:2px;' +
    'padding:3px;border-radius:10px;background:rgba(63,58,92,.07);font:500 14px/1 "Space Grotesk",sans-serif}' +
    '.tv-seg>*{padding:7px 14px;border-radius:7px;color:#8a8399;text-decoration:none;white-space:nowrap}' +
    '.tv-seg>span{background:#fff;color:#3f3a5c;box-shadow:0 1px 3px rgba(60,40,20,.14)}';
  document.head.appendChild(css);

  if (cfg.pages) {
    var seg = document.createElement('nav');
    seg.className = 'tv-seg';
    var here = location.pathname.split('/').pop();
    cfg.pages.forEach(function (p) {
      // The current page is a plain label, so the focus only ever lands on the other one.
      var el = document.createElement(p.href === here ? 'span' : 'a');
      el.textContent = p.label;
      if (el.tagName === 'A') {
        el.href = p.href;
        el.addEventListener('click', function (e) { e.preventDefault(); location.replace(el.href); });
      }
      seg.appendChild(el);
    });
    document.body.appendChild(seg);
  }

  if (!tv) return;
  var FOCUSABLE = 'button, input, select, textarea, a[href], [tabindex]';
  var lastBase = null;   // last element focused outside any popup, to return to when a popup closes
  document.documentElement.classList.add('tv-nav');

  // A thin ring in the pages' ink colour, 3px clear of the element so it also shows around dark or pink buttons.
  // It follows the focused element every frame, since some move by themselves (the labels around the clock).
  var ring = document.createElement('div');
  ring.className = 'tv-ring';
  document.body.appendChild(ring);
  var GAP = 6;   // ring width + the clear space
  var tracking = false;
  function trackRing() {
    var el = document.activeElement;
    if (!el || el === document.body || el === document.documentElement) {
      ring.style.display = 'none';
      tracking = false;
      return;
    }
    var r = el.getBoundingClientRect();
    var rad = parseFloat(getComputedStyle(el).borderTopLeftRadius) || 0;
    // A focused element that has just been hidden (a closed popup) has no box: no ring, but keep watching.
    ring.style.display = r.width < 2 || r.height < 2 ? 'none' : 'block';
    ring.style.left = (r.left - GAP) + 'px';
    ring.style.top = (r.top - GAP) + 'px';
    ring.style.width = (r.width + 2 * GAP) + 'px';
    ring.style.height = (r.height + 2 * GAP) + 'px';
    ring.style.borderRadius = (rad ? rad + GAP : 0) + 'px';
    requestAnimationFrame(trackRing);
  }
  document.addEventListener('focusin', function () {
    if (!tracking) { tracking = true; requestAnimationFrame(trackRing); }
  });

  function shown(el) {
    if (el.disabled || el.getAttribute('tabindex') === '-1' || el.closest('[hidden]')) return false;
    var r = el.getBoundingClientRect();
    if (r.width < 2 || r.height < 2) return false;
    var s = getComputedStyle(el);
    return s.visibility !== 'hidden' && s.display !== 'none';
  }

  /** The open popup the focus must stay in, or null. */
  function openScope() {
    var list = cfg.scopes || [];
    for (var i = 0; i < list.length; i++) {
      var el = document.querySelector(list[i]);
      if (el && shown(el)) return el;
    }
    return null;
  }

  function items() {
    var scope = openScope() || document;
    return Array.prototype.filter.call(scope.querySelectorAll(FOCUSABLE), shown);
  }

  function focusEl(el) {
    // Arriving on a text or number box must not pop the on-screen keyboard (it would also take the arrow keys):
    // the box stays read-only until OK.
    if (el.tagName === 'INPUT' && !el.readOnly) { el.readOnly = true; el.dataset.tvLock = '1'; }
    el.focus();
    if (el.scrollIntoView) el.scrollIntoView({ block: 'nearest', inline: 'nearest' });
  }

  /** Where the focus goes when nothing usable has it: back to the last element outside popups, or the first. */
  function restore(all) {
    if (!openScope() && lastBase && all.indexOf(lastBase) >= 0) return focusEl(lastBase);
    var first = cfg.first && document.querySelector(cfg.first);
    focusEl(first && all.indexOf(first) >= 0 ? first : all[0]);
  }

  /** Two boxes overlap in height, so they sit on one row. */
  function sameRow(a, b) {
    return b.bottom > a.top && b.top < a.bottom;
  }

  function move(dir) {
    var all = items();
    if (!all.length) return;
    var cur = document.activeElement;
    if (!cur || all.indexOf(cur) < 0) return restore(all);
    var side = dir === 'Left' || dir === 'Right';

    // Left / Right inside a group (focusable elements sharing one parent, e.g. a row of chips): the previous or
    // next one in page order, wrapped lines included. At either end of the group the focus stays.
    // A group stacked as one column (a dropdown menu) is left to Up / Down.
    if (side) {
      var group = all.filter(function (el) { return el.parentNode === cur.parentNode; });
      var isRow = group.some(function (el, i) {
        return i > 0 && sameRow(el.getBoundingClientRect(), group[i - 1].getBoundingClientRect());
      });
      if (isRow) {
        var next = group[group.indexOf(cur) + (dir === 'Right' ? 1 : -1)];
        if (next) focusEl(next);
        return;
      }
    }

    // Otherwise by position: only elements wholly on that side, and for Left / Right only ones on the same row.
    // Score = gap along the move + twice the sideways gap, so the focus keeps to its row or column.
    var a = cur.getBoundingClientRect();
    var best = null, bestScore = Infinity;
    all.forEach(function (el) {
      if (el === cur) return;
      var b = el.getBoundingClientRect();
      var main, cross;
      if (side) {
        if (!sameRow(a, b)) return;
        main = dir === 'Right' ? b.left - a.right : a.left - b.right;
        cross = 0;
      } else {
        main = dir === 'Down' ? b.top - a.bottom : a.top - b.bottom;
        cross = Math.max(0, b.left - a.right, a.left - b.right);
      }
      if (main < 0) return;
      var score = main + 2 * cross;
      if (score < bestScore) { bestScore = score; best = el; }
    });
    if (best) focusEl(best);
  }

  document.addEventListener('focusin', function (e) {
    if (!openScope()) lastBase = e.target;
  });

  document.addEventListener('keydown', function (e) {
    var k = e.key;
    if (k === 'ArrowUp' || k === 'ArrowDown' || k === 'ArrowLeft' || k === 'ArrowRight') {
      e.preventDefault();
      e.stopPropagation();
      move(k.slice(5));
    } else if (k === 'Enter') {
      var el = document.activeElement;
      // Buttons press themselves on Enter; anything else but a box being typed in gets a click.
      if (el && el.tagName === 'INPUT') {
        if (!el.readOnly) return;       // typing: the keyboard's Enter belongs to the page
        e.preventDefault();
        // OK on a locked box: make it editable and focus it again, which opens the keyboard.
        el.blur();                      // before unlocking: blurring locks it again
        el.readOnly = false;
        el.focus();
        el.click();
      } else if (el && el !== document.body && el.tagName !== 'BUTTON') {
        e.preventDefault();
        el.click();
      }
    }
  }, true);

  // Leaving a box locks it again, so the next arrival also waits for OK.
  document.addEventListener('focusout', function (e) {
    var el = e.target;
    if (el.dataset && el.dataset.tvLock) el.readOnly = true;
  });

  /** The app's Back key. True when the page closed something; false lets the app leave. */
  cfg.back = function () {
    var handled = !!(cfg.onBack && cfg.onBack());
    if (handled) setTimeout(function () {
      var all = items();
      if (all.length && all.indexOf(document.activeElement) < 0) restore(all);
    }, 0);
    return handled;
  };

  window.addEventListener('load', function () {
    setTimeout(function () {
      var all = items();
      if (all.length && all.indexOf(document.activeElement) < 0) restore(all);
    }, 300);
  });
})();
