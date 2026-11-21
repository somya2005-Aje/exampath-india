/* ExamPath India — this service worker only exists to REMOVE the old app's
   service worker (from the single-page-app version) and clear its caches.
   The website itself does not use a service worker. */
self.addEventListener("install", () => { self.skipWaiting(); });
self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.map((k) => caches.delete(k))))
      .then(() => self.registration.unregister())
  );
});
