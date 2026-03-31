/**
 * Tabiji Offline Download UI
 * Auto-detects destination pages and shows a "Download for Offline" button.
 * Communicates with the service worker via postMessage for pack management.
 */
(function () {
  'use strict';

  // Only run on destination pages: /destinations/{slug}/
  var match = window.location.pathname.match(/^\/destinations\/([^/]+)\/?$/);
  if (!match) return;
  if (!('serviceWorker' in navigator)) return;

  var destinationSlug = match[1];
  var currentPack = null;
  var containerEl = null;
  var sw = null;

  // ── Helpers ────────────────────────────────────────────

  function formatBytes(bytes) {
    if (!bytes || bytes < 1024) return bytes + ' B';
    if (bytes < 1048576) return (bytes / 1024).toFixed(0) + ' KB';
    return (bytes / 1048576).toFixed(1) + ' MB';
  }

  function getCountryFromPage() {
    // Try structured data first
    var scripts = document.querySelectorAll('script[type="application/ld+json"]');
    for (var i = 0; i < scripts.length; i++) {
      try {
        var data = JSON.parse(scripts[i].textContent);
        var loc = data.toLocation;
        if (loc && loc.containedInPlace && loc.containedInPlace.name) {
          return loc.containedInPlace.name;
        }
      } catch (e) { /* skip */ }
    }
    // Try hero badge text: "🗼 Tokyo, Japan"
    var badge = document.querySelector('.hero-badge');
    if (badge) {
      var parts = badge.textContent.split(',');
      if (parts.length >= 2) return parts[parts.length - 1].trim();
    }
    return null;
  }

  // ── Fetch packs manifest and find matching pack ────────

  function findMatchingPack(countryName) {
    return fetch('/api/v1/packs.json')
      .then(function (r) { return r.json(); })
      .then(function (data) {
        var packs = data.packs || [];
        // Find country packs that match this destination's country name
        // We match by checking pack name contains the country name
        var countryLower = countryName.toLowerCase();
        for (var i = 0; i < packs.length; i++) {
          var p = packs[i];
          if (p.packType === 'country' && p.name.toLowerCase().indexOf(countryLower) !== -1) {
            return p;
          }
        }
        // Fallback: match any pack name containing the country
        for (var j = 0; j < packs.length; j++) {
          if (packs[j].name.toLowerCase().indexOf(countryLower) !== -1) {
            return packs[j];
          }
        }
        return null;
      });
  }

  // ── Check if pack is already cached ────────────────────

  function isPackCached(packId) {
    return new Promise(function (resolve) {
      if (!sw) { resolve(false); return; }
      var handler = function (evt) {
        if (evt.data && evt.data.type === 'CACHED_PACKS') {
          navigator.serviceWorker.removeEventListener('message', handler);
          var found = (evt.data.packs || []).some(function (p) {
            return p.id === packId || ('pack:' + p.id) === packId;
          });
          resolve(found);
        }
      };
      navigator.serviceWorker.addEventListener('message', handler);
      sw.postMessage({ type: 'GET_CACHED_PACKS' });
      // Timeout fallback
      setTimeout(function () {
        navigator.serviceWorker.removeEventListener('message', handler);
        resolve(false);
      }, 3000);
    });
  }

  // ── Build UI ───────────────────────────────────────────

  function createUI(pack, isCached) {
    containerEl = document.createElement('div');
    containerEl.className = 'offline-dl';
    containerEl.setAttribute('role', 'region');
    containerEl.setAttribute('aria-label', 'Offline download');
    render(pack, isCached ? 'cached' : 'ready', 0);
    // Insert after the hero section or first h1
    var hero = document.querySelector('.hero') || document.querySelector('h1');
    if (hero && hero.parentNode) {
      hero.parentNode.insertBefore(containerEl, hero.nextSibling);
    } else {
      document.body.insertBefore(containerEl, document.body.firstChild);
    }
  }

  function render(pack, state, progress) {
    var name = pack.name || 'Travel Pack';
    var info = pack.destinationCount + ' destinations, ' + formatBytes(pack.sizeBytes);
    var html = '';

    if (state === 'ready') {
      html =
        '<div class="offline-dl-inner">' +
          '<div class="offline-dl-info">' +
            '<strong>' + name + '</strong>' +
            '<span class="offline-dl-meta">' + info + '</span>' +
          '</div>' +
          '<button class="offline-dl-btn offline-dl-btn--download" type="button">' +
            '📥 Download for Offline' +
          '</button>' +
        '</div>';
    } else if (state === 'downloading') {
      var pct = Math.round(progress);
      html =
        '<div class="offline-dl-inner">' +
          '<div class="offline-dl-info">' +
            '<strong>' + name + '</strong>' +
            '<span class="offline-dl-meta">Downloading… ' + pct + '%</span>' +
          '</div>' +
          '<div class="offline-dl-progress">' +
            '<div class="offline-dl-progress-bar" style="width:' + pct + '%"></div>' +
          '</div>' +
        '</div>';
    } else if (state === 'cached') {
      html =
        '<div class="offline-dl-inner">' +
          '<div class="offline-dl-info">' +
            '<strong>✅ ' + name + '</strong>' +
            '<span class="offline-dl-meta">Available offline · ' + info + '</span>' +
          '</div>' +
          '<button class="offline-dl-btn offline-dl-btn--remove" type="button">' +
            '🗑️ Remove' +
          '</button>' +
        '</div>';
    } else if (state === 'error') {
      html =
        '<div class="offline-dl-inner">' +
          '<div class="offline-dl-info">' +
            '<strong>' + name + '</strong>' +
            '<span class="offline-dl-meta offline-dl-meta--err">Download failed — try again</span>' +
          '</div>' +
          '<button class="offline-dl-btn offline-dl-btn--download" type="button">' +
            '📥 Retry' +
          '</button>' +
        '</div>';
    }

    containerEl.innerHTML = html;

    // Bind button events
    var dlBtn = containerEl.querySelector('.offline-dl-btn--download');
    if (dlBtn) {
      dlBtn.addEventListener('click', function () { startDownload(pack); });
    }
    var rmBtn = containerEl.querySelector('.offline-dl-btn--remove');
    if (rmBtn) {
      rmBtn.addEventListener('click', function () { removePack(pack); });
    }
  }

  // ── Download ───────────────────────────────────────────

  function startDownload(pack) {
    if (!sw) return;
    render(pack, 'downloading', 0);

    var handler = function (evt) {
      var d = evt.data;
      if (!d || !d.packId) return;
      var pid = d.packId || '';
      if (pid !== pack.id && ('pack:' + pid) !== pack.id && pid !== pack.id.replace('pack:', '')) return;

      if (d.type === 'PACK_PROGRESS') {
        var pct = 0;
        if (d.status === 'downloading') {
          pct = 10; // initial fetch
        } else if (d.status === 'caching_pages' && d.total) {
          pct = 10 + Math.round(((d.cached || 0) / d.total) * 90);
        }
        render(pack, 'downloading', pct);
      } else if (d.type === 'PACK_COMPLETE') {
        navigator.serviceWorker.removeEventListener('message', handler);
        render(pack, 'cached', 100);
      } else if (d.type === 'PACK_ERROR') {
        navigator.serviceWorker.removeEventListener('message', handler);
        render(pack, 'error', 0);
      }
    };

    navigator.serviceWorker.addEventListener('message', handler);
    sw.postMessage({
      type: 'DOWNLOAD_PACK',
      packId: pack.id,
      packUrl: pack.url
    });
  }

  // ── Remove ─────────────────────────────────────────────

  function removePack(pack) {
    if (!sw) return;
    var handler = function (evt) {
      if (evt.data && evt.data.type === 'PACK_DELETED') {
        navigator.serviceWorker.removeEventListener('message', handler);
        render(pack, 'ready', 0);
      }
    };
    navigator.serviceWorker.addEventListener('message', handler);
    sw.postMessage({ type: 'DELETE_PACK', packId: pack.id });
  }

  // ── Inject styles ──────────────────────────────────────

  function injectStyles() {
    var css =
      '.offline-dl{max-width:800px;margin:0 auto 1.5rem;padding:0 2rem}' +
      '.offline-dl-inner{background:#fff;border:1px solid var(--sand,#E8DFD0);border-radius:10px;padding:0.8rem 1rem;display:flex;align-items:center;gap:0.8rem;flex-wrap:wrap}' +
      '.offline-dl-info{flex:1;min-width:180px}' +
      '.offline-dl-info strong{display:block;font-size:0.9rem;color:var(--indigo,#2D3A5C);font-weight:600;line-height:1.3}' +
      '.offline-dl-meta{font-size:0.78rem;color:#6B5D4F;display:block;margin-top:0.15rem}' +
      '.offline-dl-meta--err{color:var(--terracotta,#C1694F)}' +
      '.offline-dl-btn{border:none;border-radius:8px;padding:0.45rem 1rem;font-size:0.82rem;font-weight:500;cursor:pointer;white-space:nowrap;font-family:inherit;transition:background 0.2s,opacity 0.2s}' +
      '.offline-dl-btn--download{background:var(--indigo,#2D3A5C);color:#fff}' +
      '.offline-dl-btn--download:hover{background:#3D4E7A}' +
      '.offline-dl-btn--remove{background:var(--warm-cream,#F5F0E8);color:var(--text,#2C2419);border:1px solid var(--sand,#E8DFD0)}' +
      '.offline-dl-btn--remove:hover{background:#ece5d9}' +
      '.offline-dl-progress{width:100%;height:6px;background:var(--sand,#E8DFD0);border-radius:3px;overflow:hidden;margin-top:0.2rem}' +
      '.offline-dl-progress-bar{height:100%;background:var(--terracotta,#C1694F);border-radius:3px;transition:width 0.3s ease}' +
      '@media(max-width:768px){.offline-dl{padding:0 1rem}.offline-dl-inner{flex-direction:column;align-items:stretch;gap:0.5rem}.offline-dl-btn{text-align:center}}';
    var style = document.createElement('style');
    style.textContent = css;
    document.head.appendChild(style);
  }

  // ── Init ───────────────────────────────────────────────

  function init() {
    navigator.serviceWorker.ready.then(function (reg) {
      sw = reg.active;
      if (!sw) return;

      var countryName = getCountryFromPage();
      if (!countryName) return;

      findMatchingPack(countryName).then(function (pack) {
        if (!pack) return;
        currentPack = pack;
        injectStyles();

        isPackCached(pack.id).then(function (cached) {
          createUI(pack, cached);
        });
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
