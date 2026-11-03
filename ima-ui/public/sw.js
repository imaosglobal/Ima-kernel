const CACHE = 'ima-shell-v8';
const SHELL = [
  '/Ima-kernel/',
  '/Ima-kernel/index.html',
  '/Ima-kernel/manifest.json'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE)
      .then(cache => cache.addAll(SHELL))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('message', event => { if (event.data?.type === 'SKIP_WAITING') self.skipWaiting(); });

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(
        keys.filter(key => key.startsWith('ima-shell-') && key !== CACHE).map(key => caches.delete(key))
      ))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;
  const url = new URL(event.request.url);
  if (url.origin !== self.location.origin) return;

  // Never let the service worker pin release metadata or the HTML shell.
  const isReleaseControl = url.pathname === '/Ima-kernel/' ||
    url.pathname === '/Ima-kernel/index.html' ||
    url.pathname === '/Ima-kernel/version.json';

  event.respondWith(
    fetch(event.request, { cache: 'no-store' })
      .then(response => {
        if (!isReleaseControl && response.ok) {
          const copy = response.clone();
          caches.open(CACHE).then(cache => cache.put(event.request, copy));
        }
        return response;
      })
      .catch(() => caches.match(event.request).then(cached => cached || caches.match('/Ima-kernel/')))
  );
});
