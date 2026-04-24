// PWA removed 2026-04-23. This stub exists only to clean up service workers
// that were registered in returning visitors' browsers. Once installed, it
// clears all caches and unregisters itself, then passes through every fetch.
// Safe to delete this file after a few months once browser caches have aged out.

self.addEventListener('install', () => self.skipWaiting());

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.map((k) => caches.delete(k))))
      .then(() => self.registration.unregister())
      .then(() => self.clients.matchAll())
      .then((clients) => clients.forEach((c) => c.navigate(c.url)))
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(fetch(event.request));
});
