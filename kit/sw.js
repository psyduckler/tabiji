const CACHE_NAME = 'tabiji-kit-v1';
const APP_SHELL = [
  '/kit/',
  '/kit/index.html',
  '/kit/app.js',
  '/kit/style.css',
  '/kit/manifest.json',
  '/kit/data/countries.json',
  '/kit/icons/icon-192.png',
  '/kit/icons/icon-512.png',
];

const FONT_URLS = [
  'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap',
];

// Install: cache app shell
self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(APP_SHELL);
    }).then(() => self.skipWaiting())
  );
});

// Activate: clean old caches
self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

// Fetch: network-first for data, cache-first for app shell
self.addEventListener('fetch', (e) => {
  const url = new URL(e.request.url);

  // Google Fonts — cache first, fallback to network
  if (url.hostname === 'fonts.googleapis.com' || url.hostname === 'fonts.gstatic.com') {
    e.respondWith(
      caches.match(e.request).then((cached) => {
        if (cached) return cached;
        return fetch(e.request).then((res) => {
          const clone = res.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(e.request, clone));
          return res;
        });
      })
    );
    return;
  }

  // Country data files — serve from cache if available (user downloaded), else network
  if (url.pathname.startsWith('/kit/data/safety/')) {
    e.respondWith(
      caches.match(e.request).then((cached) => {
        if (cached) return cached;
        return fetch(e.request);
      })
    );
    return;
  }

  // App shell — cache first, fallback network
  if (APP_SHELL.includes(url.pathname)) {
    e.respondWith(
      caches.match(e.request).then((cached) => {
        const fetchPromise = fetch(e.request).then((res) => {
          const clone = res.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(e.request, clone));
          return res;
        }).catch(() => cached);
        return cached || fetchPromise;
      })
    );
    return;
  }

  // Everything else — network first
  e.respondWith(
    fetch(e.request).catch(() => caches.match(e.request))
  );
});

// Message handler for caching country data
self.addEventListener('message', (e) => {
  if (e.data && e.data.type === 'CACHE_COUNTRY') {
    const url = e.data.url;
    caches.open(CACHE_NAME).then((cache) => {
      fetch(url).then((res) => {
        cache.put(url, res).then(() => {
          e.source.postMessage({ type: 'COUNTRY_CACHED', iso2: e.data.iso2 });
        });
      }).catch(() => {
        e.source.postMessage({ type: 'CACHE_ERROR', iso2: e.data.iso2 });
      });
    });
  }

  if (e.data && e.data.type === 'UNCACHE_COUNTRY') {
    const url = e.data.url;
    caches.open(CACHE_NAME).then((cache) => {
      cache.delete(url).then(() => {
        e.source.postMessage({ type: 'COUNTRY_UNCACHED', iso2: e.data.iso2 });
      });
    });
  }
});
