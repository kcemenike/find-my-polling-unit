var CACHE = 'pu-map-v3';

var SHELL = [
  './',
  './index.html',
  './manifest.webmanifest',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './lib/leaflet.css',
  './lib/leaflet.js',
  './lib/leaflet.markercluster.js',
  './lib/MarkerCluster.css',
  './lib/MarkerCluster.Default.css',
  './lib/images/marker-icon.png',
  './lib/images/marker-icon-2x.png',
  './lib/images/marker-shadow.png',
  './votendc.jpg'
];

var STATES = [
  'abia','adamawa','akwa-ibom','anambra','bauchi','bayelsa','benue','borno',
  'cross-river','delta','ebonyi','edo','ekiti','enugu','fct','gombe','imo',
  'jigawa','kaduna','kano','katsina','kebbi','kogi','kwara','lagos','nasarawa',
  'niger','ogun','ondo','osun','oyo','plateau','rivers','sokoto','taraba','yobe','zamfara'
];

var DATA = [
  './pu/index.json',
  './ward.json',
  './lga.json',
  './state.json',
  './nat.json'
].concat(STATES.map(function(s) { return './pu/' + s + '.json'; }));

self.addEventListener('install', function (event) {
  event.waitUntil(
    caches.open(CACHE).then(function (cache) {
      return Promise.all(
        SHELL.concat(DATA).map(function (url) {
          return cache.add(new Request(url, { cache: 'reload' })).catch(function () {});
        })
      );
    }).then(function () {
      return self.skipWaiting();
    })
  );
});

self.addEventListener('activate', function (event) {
  event.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(
        keys.map(function (key) {
          return key === CACHE ? null : caches.delete(key);
        })
      );
    }).then(function () {
      return self.clients.claim();
    })
  );
});

self.addEventListener('message', function (event) {
  if (event.data === 'skip-waiting') self.skipWaiting();
});

self.addEventListener('fetch', function (event) {
  var request = event.request;
  if (request.method !== 'GET') return;

  var url = new URL(request.url);
  var sameOrigin = url.origin === self.location.origin;

  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request).then(function (response) {
        var copy = response.clone();
        caches.open(CACHE).then(function (cache) {
          cache.put('./index.html', copy);
        });
        return response;
      }).catch(function () {
        return caches.match('./index.html').then(function (hit) {
          return hit || caches.match('./');
        });
      })
    );
    return;
  }

  // Google map tiles: try network, fall back to cache (tiles viewed before)
  if (/^mt\d\.google\.com$/.test(url.hostname)) {
    event.respondWith(
      fetch(request).then(function (response) {
        if (response && response.ok) {
          var copy = response.clone();
          caches.open(CACHE).then(function (cache) {
            cache.put(request, copy);
          });
        }
        return response;
      }).catch(function () {
        return caches.match(request);
      })
    );
    return;
  }

  if (!sameOrigin) return;

  // Same-origin assets: serve from cache, refresh in background
  event.respondWith(
    caches.match(request).then(function (hit) {
      var network = fetch(request).then(function (response) {
        if (response && response.ok) {
          var copy = response.clone();
          caches.open(CACHE).then(function (cache) {
            cache.put(request, copy);
          });
        }
        return response;
      }).catch(function () {
        return hit;
      });
      return hit || network;
    })
  );
});
