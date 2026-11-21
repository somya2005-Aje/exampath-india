# ExamPath India — Android app (Capacitor)

User App wrapper around `../final-deploy/` (the website, no login).
appId `com.exampathindia.app`, appName "ExamPath India", v1.1.0.

Build: GitHub Actions (`.github/workflows/build-apk.yml`) — push to main builds
the debug APK and uploads it as artifact `exampath-apk`. Local Gradle build is
blocked on this VM (runtime blocks loopback TCP, Gradle daemon cannot run).

Prepare web assets: `bash scripts/prepare-www.sh` (copies final-deploy → www).
Sync: `cd android-app && npx cap sync android`.
