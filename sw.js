/**
 * Tabiji Service Worker
 * Cache-first app shell, network-first pages, region pack downloads
 */

const CACHE_VERSION = 'tabiji-v1';
const SHELL_CACHE = `shell-${CACHE_VERSION}`;
const PAGE_CACHE = `pages-${CACHE_VERSION}`;
const API_CACHE = `api-${CACHE_VERSION}`;
const PACK_CACHE = `packs-${CACHE_VERSION}`;
const FONT_CACHE = `fonts-${CACHE_VERSION}`;

const SHELL_ASSETS = [
  '/assets/shared-shell.css',
  '/assets/shared-shell.js',
  '/manifest.json',
  '/favicon.ico',
  '/offline.html'
];

const SHELL_EXTERNAL = [
  'https://img.tabiji.ai/icon-192.png',
  'https://img.tabiji.ai/icon-512.png',
  'https://img.tabiji.ai/apple-touch-icon.png'
];

const API_URLS = [
  '/api/v1/filter.json',
  '/api/v1/facets.json',
  '/api/v1/packs.json',
  '/api/v1/manifest.json'
];

// ── Install ──────────────────────────────────────────────
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(SHELL_CACHE).then(cache =>
      cache.addAll(SHELL_ASSETS).catch(() => {
        // Cache what we can; don't fail install for missing optional assets
        return Promise.allSettled(SHELL_ASSETS.map(url => cache.add(url)));
      })
    ).then(() =>
      caches.open(SHELL_CACHE).then(cache =>
        Promise.allSettled(SHELL_EXTERNAL.map(url => cache.add(url)))
      )
    ).then(() => self.skipWaiting())
  );
});

// ── Activate ─────────────────────────────────────────────
self.addEventListener('activate', event => {
  const currentCaches = [SHELL_CACHE, PAGE_CACHE, API_CACHE, PACK_CACHE, FONT_CACHE];
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys
          .filter(key => !currentCaches.includes(key))
          .map(key => caches.delete(key))
      )
    ).then(() => self.clients.claim())
  );
});

// ── Fetch ────────────────────────────────────────────────
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);

  // Only handle GET
  if (request.method !== 'GET') return;

  // Google Fonts — cache-first
  if (url.hostname === 'fonts.googleapis.com' || url.hostname === 'fonts.gstatic.com') {
    event.respondWith(cacheFirst(request, FONT_CACHE));
    return;
  }

  // R2 icons — cache-first
  if (url.hostname === 'img.tabiji.ai') {
    event.respondWith(cacheFirst(request, SHELL_CACHE));
    return;
  }

  // Only handle same-origin from here
  if (url.origin !== self.location.origin) return;

  // Shell assets — cache-first
  if (SHELL_ASSETS.includes(url.pathname)) {
    event.respondWith(cacheFirst(request, SHELL_CACHE));
    return;
  }

  // API data — stale-while-revalidate
  if (url.pathname.startsWith('/api/v1/') && !url.pathname.match(/\/api\/v1\/packs\/[^/]+\.json/)) {
    event.respondWith(staleWhileRevalidate(request, API_CACHE));
    return;
  }

  // Pack data — cache-first (explicitly downloaded)
  if (url.pathname.match(/\/api\/v1\/packs\/[^/]+\.json/)) {
    event.respondWith(cacheFirst(request, PACK_CACHE));
    return;
  }

  // HTML pages — network-first with offline fallback
  if (request.headers.get('Accept')?.includes('text/html') || url.pathname.endsWith('/') || url.pathname.endsWith('.html')) {
    event.respondWith(networkFirstPage(request));
    return;
  }

  // Everything else — network with cache fallback
  event.respondWith(
    fetch(request).catch(() => caches.match(request))
  );
});

// ── Message handler (pack downloads) ─────────────────────
self.addEventListener('message', event => {
  const { type, packUrl, packId } = event.data || {};

  if (type === 'DOWNLOAD_PACK' && packUrl) {
    event.waitUntil(
      downloadPack(packUrl, packId, event.source)
    );
  }

  if (type === 'GET_CACHED_PACKS') {
    event.waitUntil(
      getCachedPacks().then(packs => {
        event.source.postMessage({ type: 'CACHED_PACKS', packs });
      })
    );
  }

  if (type === 'GET_CACHED_PAGES') {
    event.waitUntil(
      getCachedPages().then(pages => {
        event.source.postMessage({ type: 'CACHED_PAGES', pages });
      })
    );
  }

  if (type === 'DELETE_PACK' && packId) {
    event.waitUntil(
      caches.open(PACK_CACHE).then(cache => {
        const packUrl2 = `/api/v1/packs/${packId}.json`;
        return cache.delete(packUrl2);
      }).then(() => {
        event.source.postMessage({ type: 'PACK_DELETED', packId });
      })
    );
  }
});

// ── Strategies ───────────────────────────────────────────

async function cacheFirst(request, cacheName) {
  const cached = await caches.match(request);
  if (cached) return cached;
  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(cacheName);
      cache.put(request, response.clone());
    }
    return response;
  } catch {
    return new Response('', { status: 503, statusText: 'Offline' });
  }
}

async function staleWhileRevalidate(request, cacheName) {
  const cache = await caches.open(cacheName);
  const cached = await cache.match(request);

  const fetchPromise = fetch(request).then(response => {
    if (response.ok) {
      cache.put(request, response.clone());
    }
    return response;
  }).catch(() => cached);

  return cached || fetchPromise;
}

async function networkFirstPage(request) {
  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(PAGE_CACHE);
      cache.put(request, response.clone());
    }
    return response;
  } catch {
    const cached = await caches.match(request);
    if (cached) return cached;
    return caches.match('/offline.html');
  }
}

// ── Pack download ────────────────────────────────────────

async function downloadPack(packUrl, packId, client) {
  try {
    // Notify start
    client?.postMessage({ type: 'PACK_PROGRESS', packId, status: 'downloading' });

    const cache = await caches.open(PACK_CACHE);
    const response = await fetch(packUrl);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);

    await cache.put(packUrl, response.clone());

    // Try to pre-cache destination pages from the pack
    const packData = await response.json();
    if (packData.destinations && Array.isArray(packData.destinations)) {
      client?.postMessage({ type: 'PACK_PROGRESS', packId, status: 'caching_pages', total: packData.destinations.length });

      const pageCache = await caches.open(PAGE_CACHE);
      let cached = 0;

      // Cache in batches of 10 to avoid overwhelming the network
      const slugs = packData.destinations.map(d => d.slug).filter(Boolean);
      for (let i = 0; i < slugs.length; i += 10) {
        const batch = slugs.slice(i, i + 10);
        const results = await Promise.allSettled(
          batch.map(async slug => {
            const pageUrl = `/${slug}/`;
            const pageResp = await fetch(pageUrl);
            if (pageResp.ok) {
              await pageCache.put(pageUrl, pageResp);
            }
          })
        );
        cached += results.filter(r => r.status === 'fulfilled').length;
        client?.postMessage({ type: 'PACK_PROGRESS', packId, status: 'caching_pages', cached, total: slugs.length });
      }
    }

    client?.postMessage({ type: 'PACK_COMPLETE', packId });
  } catch (err) {
    client?.postMessage({ type: 'PACK_ERROR', packId, error: err.message });
  }
}

async function getCachedPacks() {
  try {
    const cache = await caches.open(PACK_CACHE);
    const keys = await cache.keys();
    const packs = [];
    for (const request of keys) {
      const url = new URL(request.url);
      if (url.pathname.match(/\/api\/v1\/packs\/[^/]+\.json/)) {
        const id = url.pathname.split('/').pop().replace('.json', '');
        packs.push({ id, url: url.pathname });
      }
    }
    return packs;
  } catch {
    return [];
  }
}

async function getCachedPages() {
  try {
    const cache = await caches.open(PAGE_CACHE);
    const keys = await cache.keys();
    return keys.map(req => {
      const url = new URL(req.url);
      return url.pathname;
    }).filter(p => p !== '/offline.html');
  } catch {
    return [];
  }
}
