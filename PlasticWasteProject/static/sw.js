const CACHE_NAME = 'smartwaste-v1';
const ASSETS = [
  '/',
  '/static/landing.css',
  '/static/index.css',
  '/static/dashboard.css',
  '/static/main.js'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request);
    })
  );
});