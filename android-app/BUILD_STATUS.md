# DailyTools Android APK — Build Status

**Date:** 2026-11-21
**Version:** 1.0.0 (`com.dailytools.app`, versionCode 1)
**Result: NO APK BUILT LOCALLY — blocked by the runtime's raw-TCP block (see below).**
The GitHub Actions fallback is ready; that is the way to get the APK.

## What is ready (verified on disk)

- `android-app/` — complete Capacitor 8.6.0 project (copied from the proven
  `ai-universe/android-app/` pattern and adapted: appId `com.dailytools.app`,
  appName `DailyTools`, MainActivity in `com.dailytools.app`).
- `android-app/www/` — 12 files, copy of `final-deploy/` (latest indigo /
  dark-theme design); the app runs from local files, no live-site dependency.
- `npx cap sync android` — passes; web assets copied into
  `android/app/src/main/assets/public/`.
- Icons — 512×512 master (`android-app/icon-512.png`) + all mipmap densities
  (launcher / foreground / round) and port+land splash screens, indigo palette
  matching the live site (#4F46E5 / #818CF8, dark splash #0B1220).
- `android-app/scripts/prepare-www.sh` and `scripts/build_apk.sh` — ready.
- `android-app/README.md` — rebuild instructions.
- `.github/workflows/build-apk.yml` — GitHub Actions debug-APK build
  (no secrets needed for debug).
- Toolchain installed on this VM: JDK 21 (`/usr/lib/jvm/java-21-openjdk-amd64`),
  Android SDK at `~/Android/sdk` (platforms android-35/36, build-tools 35/36),
  Gradle 8.14.3 distribution downloaded + verified at
  `~/.gradle/wrapper/dists/gradle-8.14.3-all/10utluxaxniiv4wxiphsi49nj/`.

## Exact local-build blocker (one attempt, then stopped per instructions)

Command: `bash android-app/scripts/build_apk.sh`
(`./gradlew assembleDebug --no-daemon -Dorg.gradle.daemon=false`,
`JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64`,
`ANDROID_HOME=$HOME/Android/sdk`, `GRADLE_USER_HOME=$HOME/.gradle`)

Failure:

```
To honour the JVM settings for this build a single-use Daemon process will be forked.
FAILURE: Build failed with an exception.
* What went wrong:
The first result from the daemon was empty. The daemon process may have died
or a non-daemon process is reusing the same port.
```

Cause: the runtime blocks raw TCP connections, including loopback
(127.0.0.1). Gradle 8's `--no-daemon` still forks a single-use daemon and
talks to it over a loopback TCP socket, so the client never receives the
daemon's first result. This is the same documented block as in `~/AGENTS.md`
("Gradle daemon / raw TCP block"): the fix is to set Muse Settings →
Permissions → Direct network protocols → `other_tcp` Deny → Ask, then retry
`bash android-app/scripts/build_apk.sh`. Two earlier sub-problems were fixed
along the way and are NOT the blocker: no JDK (installed openjdk-21 via apt)
and the wrapper's 10 s download timeout (bumped to 300 s; Gradle 8.14.3 was
then fetched with curl, which survives the proxy where Java's downloader
does not — `Connection reset`).

Do NOT loop local retries while `other_tcp` is Deny — every attempt fails
the same way.

## How to get the APK (GitHub Actions — recommended)

1. Push `~/workspace/dailytools/` to a GitHub repo (e.g.
   `somya2005-Aje/dailytools`), including `android-app/` and `.github/`.
   Do NOT commit any keystore (none exists yet; debug needs none).
2. GitHub → repo → Actions tab → "Build DailyTools debug APK" → Run workflow
   (it also runs on every push to `main`).
3. When the run finishes, download the `dailytools-apk` artifact — it
   contains `app-debug.apk` (debug-signed, installs on a phone with
   "Install unknown apps" allowed; not Play Store ready).
4. Host that APK at `https://dailytools-o5b.pages.dev/dailytools.apk`
   (copy into `final-deploy/` and redeploy the Pages site) so the website's
   Download button serves the real file.

## For a signed release APK later

Generate a release keystore (`keytool -genkeypair ...`), add it as repo
secrets (`KEYSTORE_BASE64` / `KEYSTORE_PASSWORD` / `KEY_ALIAS`), restore it
in the workflow before the build step, and run `./gradlew assembleRelease`
instead of `assembleDebug` — the proven pattern is in
`~/workspace/voiceworld-ai/.github/workflows/build-apk.yml`.

## Update 2026-11-21 20:38 IST — APK BUILT ✅
- Built via GitHub Actions (repo somya2005-Aje/dailytools, run 44917455232, push to main). Local build still blocked by the runtime TCP rule — use Actions.
- APK: `dailytools.apk` (4,228,658 bytes, debug-signed, sideload only), package `com.dailytools.app`, v1.0.0, label DailyTools.
- Verified inside the APK: full v2 web app (110 tools, 15 categories), Roman Hindi UI ("Aapke Saare Daily Tools"), zero Devanagari.
- Also hosted at https://dailytools-o5b.pages.dev/dailytools.apk
