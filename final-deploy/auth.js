/* ExamPath India — auth.js — REAL auth only. No demo login, no fake "logged in" state, no local password login.
   How it works:
   - This module waits for window.FIREBASE_CONFIG (the Firebase web config object).
     The Firebase setup runs separately; until that config is provided, Google Sign-In
     is NOT available and the login box says so honestly.
   - When FIREBASE_CONFIG exists, the Firebase SDK is loaded from Google, and
     "Sign in with Google" performs a REAL Google sign-in (signInWithPopup).
   - The login session flag in localStorage ("ep_auth_session") is written ONLY after
     a real Firebase sign-in succeeds. Without a config, any stale flag is cleared.
   - What login unlocks: paper Downloads and full exam details (pattern, syllabus,
     complete numbered paper list). Paper photo-cards, home, search and YouTube stay
     free without login. */
(function () {
  "use strict";
  var KEY = "ep_auth_session";
  var pendingAction = null;

  function $(s) { return document.querySelector(s); }
  function $all(s) { return Array.prototype.slice.call(document.querySelectorAll(s)); }

  function getSession() {
    try { return JSON.parse(localStorage.getItem(KEY) || "null"); } catch (e) { return null; }
  }
  function setSession(s) {
    try { if (s) { localStorage.setItem(KEY, JSON.stringify(s)); } else { localStorage.removeItem(KEY); } } catch (e) {}
  }
  function isLoggedIn() { return !!getSession(); }
  function getUser() { return getSession(); }
  function hasConfig() { return !!(window.FIREBASE_CONFIG && window.FIREBASE_CONFIG.apiKey); }

  function toast(m) {
    if (window.toast) { window.toast(m); return; }
    var t = $("#toast");
    if (t) { t.textContent = m; t.style.display = "block"; setTimeout(function () { t.style.display = "none"; }, 2600); }
  }

  /* ---------- login modal (built once) ---------- */
  function ensureModal() {
    var ov = $("#authOverlay");
    if (ov) return ov;
    ov = document.createElement("div");
    ov.className = "auth-overlay";
    ov.id = "authOverlay";
    ov.hidden = true;
    ov.innerHTML =
      '<div class="auth-box" role="dialog" aria-modal="true" aria-label="Login">' +
      '<button class="auth-close" id="authClose" type="button" aria-label="Close">✕</button>' +
      '<h3>🔐 Login to ExamPath India</h3>' +
      '<p class="small" id="authWhy">Login to download papers and see full exam details.</p>' +
      '<button class="auth-google" id="authGoogleBtn" type="button"></button>' +
      '<p class="small" id="authNote"></p>' +
      '<p class="small">No password here — Google sign-in only. Paper photos, home, search and videos stay free without login.</p>' +
      '</div>';
    document.body.appendChild(ov);
    ov.addEventListener("click", function (e) { if (e.target === ov) closeLogin(); });
    $("#authClose").addEventListener("click", closeLogin);
    $("#authGoogleBtn").addEventListener("click", onGoogleClick);
    return ov;
  }

  function openLogin(why) {
    var ov = ensureModal();
    if (why) { var w = $("#authWhy"); if (w) w.textContent = why; }
    var btn = $("#authGoogleBtn"), note = $("#authNote");
    if (hasConfig()) {
      btn.textContent = "Sign in with Google";
      btn.disabled = false;
      note.textContent = "";
    } else {
      btn.textContent = "Google sign-in setup ho raha hai — thodi der me check karein";
      btn.disabled = false;
      note.textContent = "Google sign-in abhi setup ho raha hai. Firebase config milte hi asli Google login khul jayega. Abhi aap logged in nahi hain — koi fake login nahi banaya gaya hai.";
    }
    ov.hidden = false;
  }

  function closeLogin() {
    var ov = $("#authOverlay");
    if (ov) ov.hidden = true;
  }

  /* ---------- real Firebase Google sign-in (only when config exists) ---------- */
  function loadScript(src) {
    return new Promise(function (res, rej) {
      var s = document.createElement("script");
      s.src = src; s.onload = res;
      s.onerror = function () { rej(new Error("Failed to load " + src)); };
      document.head.appendChild(s);
    });
  }
  var firebaseReady = null;
  function ensureFirebase() {
    if (firebaseReady) return firebaseReady;
    firebaseReady = loadScript("https://www.gstatic.com/firebasejs/10.12.2/firebase-app-compat.js")
      .then(function () { return loadScript("https://www.gstatic.com/firebasejs/10.12.2/firebase-auth-compat.js"); })
      .then(function () {
        if (!window.firebase.apps.length) window.firebase.initializeApp(window.FIREBASE_CONFIG);
        return window.firebase.auth();
      });
    return firebaseReady;
  }

  function onGoogleClick() {
    var note = $("#authNote"), btn = $("#authGoogleBtn");
    if (!hasConfig()) {
      if (note) note.textContent = "Google sign-in abhi setup ho raha hai. Firebase config milte hi asli Google login khul jayega. Abhi aap logged in nahi hain — koi fake login nahi banaya gaya hai.";
      return;
    }
    btn.disabled = true;
    if (note) note.textContent = "Google sign-in khul raha hai…";
    ensureFirebase().then(function (auth) {
      return auth.signInWithPopup(new window.firebase.auth.GoogleAuthProvider());
    }).then(function (result) {
      var u = result.user;
      setSession({ uid: u.uid, name: u.displayName || "", photo: u.photoURL || "", email: u.email || "" });
      closeLogin();
      updateHeader();
      updateLocks();
      toast("Logged in as " + (u.displayName || u.email || "Google user") + " ✓");
      if (pendingAction) { var fn = pendingAction; pendingAction = null; fn(); }
    }).catch(function (err) {
      btn.disabled = false;
      if (note) note.textContent = "Sign-in nahi ho paya: " + (err && err.message ? err.message : "unknown error") + " Dobara try karein.";
    });
  }

  function logout() {
    if (hasConfig()) {
      ensureFirebase().then(function (auth) { return auth.signOut(); }).catch(function () {});
    }
    setSession(null);
    pendingAction = null;
    updateHeader();
    updateLocks();
    toast("Logged out");
  }

  function requireLogin(why, fn) {
    if (isLoggedIn()) { if (fn) fn(); return; }
    pendingAction = fn || null;
    openLogin(why || "Login to continue.");
  }

  /* ---------- header (name/photo + logout) & locked sections ---------- */
  function updateHeader() {
    var area = $("#authArea");
    var u = getUser();
    if (area) {
      if (u) {
        area.innerHTML =
          '<span class="auth-userchip">' +
          (u.photo ? '<img src="' + u.photo.replace(/"/g, "") + '" alt="" onerror="this.style.display=\'none\'">' : "") +
          '<span>' + (u.name || u.email || "User").replace(/</g, "&lt;") + '</span>' +
          '<button class="btn sm ghost" type="button" data-auth-logout>Logout</button></span>';
      } else {
        area.innerHTML = '<a class="login-pill" href="/profile" data-auth-login>👤 Login / Sign Up</a>';
      }
    }
    $all("[data-auth-login]").forEach(function (el) {
      if (el.closest("#authArea")) return;
      if (u) { el.textContent = "👤 " + (u.name || "My Account").split(" ")[0]; }
      else if (el.getAttribute("href") === "/profile") { el.textContent = "👤 Login / Sign Up"; }
    });
  }

  function updateLocks() {
    var on = isLoggedIn();
    $all(".locked-detail").forEach(function (el) { el.classList.toggle("unlocked", on); });
  }

  /* ---------- delegated clicks: login / logout / gated downloads ---------- */
  document.addEventListener("click", function (e) {
    var loginBtn = e.target.closest("[data-auth-login]");
    if (loginBtn) { e.preventDefault(); openLogin(); return; }
    var logoutBtn = e.target.closest("[data-auth-logout]");
    if (logoutBtn) { e.preventDefault(); logout(); return; }
    var dl = e.target.closest("[data-download-url]");
    if (dl) {
      e.preventDefault();
      var url = dl.getAttribute("data-download-url");
      requireLogin("Login to download this paper.", function () { window.open(url, "_blank"); });
      return;
    }
  });

  /* ---------- init ---------- */
  function init() {
    if (!hasConfig()) {
      // No Firebase config yet: no real sign-in is possible, so drop any stale flag.
      setSession(null);
    }
    updateHeader();
    updateLocks();
    if (hasConfig()) {
      ensureFirebase().then(function (auth) {
        auth.onAuthStateChanged(function (user) {
          if (user) {
            setSession({ uid: user.uid, name: user.displayName || "", photo: user.photoURL || "", email: user.email || "" });
          } else {
            setSession(null);
          }
          updateHeader();
          updateLocks();
        });
      }).catch(function () { /* SDK failed to load; login stays unavailable, honestly. */ });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  window.ExamPathAuth = {
    isLoggedIn: isLoggedIn,
    getUser: getUser,
    hasConfig: hasConfig,
    openLogin: openLogin,
    closeLogin: closeLogin,
    logout: logout,
    requireLogin: requireLogin,
    updateHeader: updateHeader,
    updateLocks: updateLocks
  };
})();
