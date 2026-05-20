const CACHE_NAME = 'acadstat-v1';
const OFFLINE_URL = '/';
const ASSETS_TO_CACHE = [
    '/',
    '/static/css/style.css',
    '/static/js/script.js',
    '/manifest.json',
    'https://cdn.jsdelivr.net/npm/chart.js',
    'https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css',
    'https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js',
    'https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap',
];

// Install: cache the core shell
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => {
            return cache.addAll(ASSETS_TO_CACHE);
        }).then(() => self.skipWaiting())
    );
});

// Activate: purge old caches
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(keys =>
            Promise.all(
                keys.filter(key => key !== CACHE_NAME)
                    .map(key => caches.delete(key))
            )
        ).then(() => self.clients.claim())
    );
});

// Fetch: network-first for API, cache-first for assets
self.addEventListener('fetch', event => {
    const { request } = event;
    const url = new URL(request.url);

    // Skip non-GET requests
    if (request.method !== 'GET') return;

    // API routes → network only (no caching)
    if (url.pathname.startsWith('/api/') ||
        url.pathname.startsWith('/login/') ||
        url.pathname.startsWith('/logout/') ||
        url.pathname.startsWith('/send-message/') ||
        url.pathname.startsWith('/lock-result/') ||
        url.pathname.startsWith('/unlock-result/') ||
        url.pathname.startsWith('/mark-notification-read/') ||
        url.pathname.startsWith('/mark-all-notifications-read/') ||
        url.pathname.startsWith('/milestone-check/')) {
        event.respondWith(fetch(request).catch(() => caches.match(OFFLINE_URL)));
        return;
    }

    // Static assets → cache-first
    if (url.origin === location.origin && url.pathname.startsWith('/static/')) {
        event.respondWith(
            caches.match(request).then(cached => cached || fetch(request).then(resp => {
                if (resp.ok) {
                    const clone = resp.clone();
                    caches.open(CACHE_NAME).then(cache => cache.put(request, clone));
                }
                return resp;
            }))
        );
        return;
    }

    // HTML pages → stale-while-revalidate
    event.respondWith(
        caches.match(request).then(cached => {
            const networkFetch = fetch(request).then(resp => {
                if (resp.ok) {
                    caches.open(CACHE_NAME).then(cache => cache.put(request, resp.clone()));
                }
                return resp;
            }).catch(() => cached);
            return cached || networkFetch;
        })
    );
});

self.addEventListener('message', event => {
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
});
