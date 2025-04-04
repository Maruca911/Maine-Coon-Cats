const CACHE_NAME = 'catcare-v1';
const urlsToCache = [
    '/',
    '/index.html',
    '/css/style.css',
    '/css/article.css',
    '/js/main.js',
    '/js/search.js',
    '/js/comments.js',
    '/js/utils.js',
    '/images/logo.png',
    '/images/icon-192x192.png',
    '/images/icon-512x512.png',
    '/about.html',
    '/contact.html',
    '/privacy.html',
    '/impressum.html',
    '/blog/index.html',
    '/blog/templates/article.html',
    '/sitemap.xml',
    '/robots.txt',
    '/manifest.json'
];

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                return cache.addAll(urlsToCache);
            })
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                if (response) {
                    return response;
                }
                return fetch(event.request)
                    .then(response => {
                        if (!response || response.status !== 200 || response.type !== 'basic') {
                            return response;
                        }
                        const responseToCache = response.clone();
                        caches.open(CACHE_NAME)
                            .then(cache => {
                                cache.put(event.request, responseToCache);
                            });
                        return response;
                    });
            })
    );
});

self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheName !== CACHE_NAME) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
}); 