/* Remote (D-pad) control for the kids' pages, used only inside the "Đồng Hồ" TV app (tre-em/android), which
 * adds "TVApp/" to the user agent. In a browser this file does nothing, so phones and computers are unchanged.
 *
 * - Arrow keys move the focus to the nearest focusable element in that direction (buttons, inputs, and anything
 *   with a tabindex), only inside an open popup when the page lists one in TVNav.scopes.
 * - OK (Enter) presses the focused element; buttons do that by themselves, other elements get a click().
 * - The app's Back key calls TVNav.back(): the page's TVNav.onBack() closes what is open and returns true;
 *   false lets the app go back to the TV's home screen.
 *
 * - TVNav.pages adds a small switch at the top centre, drawn like the Chat / Code switch of the Claude desktop
 *   app: a soft grey track, the current page on a raised white segment. The other segment opens its page in place
 *   of this one, so the app's history stays one page deep and Back always leaves the app.
 *
 * A page sets window.TVNav = { scopes: [...popup selectors...], onBack: function(){...}, first: 'selector',
 * pages: [{ href: 'page.html', label: 'Name' }, ...] } before loading this file. */
(function () {
  if (!/TVApp\//.test(navigator.userAgent)) return;
  var cfg = window.TVNav = window.TVNav || {};
  var FOCUSABLE = 'button, input, select, textarea, a[href], [tabindex]';
  var lastBase = null;   // last element focused outside any popup, to return to when a popup closes

  document.documentElement.classList.add('tv-nav');
  var css = document.createElement('style');
  // A thin ring in the pages' ink colour, with a cream gap so it also shows around dark or pink buttons.
  css.textContent = '.tv-nav :focus{outline:3px solid #2b2b33 !important;outline-offset:3px !important}' +
    '.tv-seg{position:fixed;top:14px;left:50%;transform:translateX(-50%);z-index:50;display:flex;gap:2px;' +
    'padding:3px;border-radius:10px;background:rgba(63,58,92,.07);font:500 14px/1 "Space Grotesk",sans-serif}' +
    '.tv-seg>*{padding:7px 14px;border-radius:7px;color:#8a8399;text-decoration:none}' +
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

  function move(dir) {
    var all = items();
    if (!all.length) return;
    var cur = document.activeElement;
    if (!cur || all.indexOf(cur) < 0) return restore(all);
    var a = cur.getBoundingClientRect();
    var ax = a.left + a.width / 2, ay = a.top + a.height / 2;
    var best = null, bestScore = Infinity;
    all.forEach(function (el) {
      if (el === cur) return;
      var b = el.getBoundingClientRect();
      var dx = b.left + b.width / 2 - ax, dy = b.top + b.height / 2 - ay;
      var main, cross;
      // Only elements that lie in the pressed direction; cross-axis distance counts double so the focus
      // keeps to its row or column instead of jumping diagonally.
      if (dir === 'Right') { if (b.left < a.right - 4 && dx <= 4) return; main = dx; cross = Math.abs(dy); }
      else if (dir === 'Left') { if (b.right > a.left + 4 && dx >= -4) return; main = -dx; cross = Math.abs(dy); }
      else if (dir === 'Down') { if (b.top < a.bottom - 4 && dy <= 4) return; main = dy; cross = Math.abs(dx); }
      else { if (b.bottom > a.top + 4 && dy >= -4) return; main = -dy; cross = Math.abs(dx); }
      if (main <= 0) return;
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
