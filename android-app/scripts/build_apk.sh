#!/usr/bin/env bash
# Build the DailyTools debug APK (Capacitor 8 wrapper around final-deploy/).
#
# Requirements: Node 22+, JDK 21, Android SDK (platforms;android-36,
# build-tools;36.0.0). On this VM the SDK already lives at ~/Android/sdk.
#
# KNOWN ISSUE: the runtime blocks raw TCP (including loopback), and the
# Gradle daemon talks to its client over a loopback TCP socket. Gradle 9
# always forks a daemon, so use --no-daemon (Gradle 8 runs in-process then).
# If the build still fails with "Could not dispatch a message to the daemon"
# / Broken pipe, do NOT loop retries — see BUILD_STATUS.md and use the
# GitHub Actions workflow instead.
#
# Usage: bash android-app/scripts/build_apk.sh   (run from the repo root)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
APP="$ROOT/android-app"

export ANDROID_HOME="${ANDROID_HOME:-$HOME/Android/sdk}"
export ANDROID_SDK_ROOT="$ANDROID_HOME"
export JAVA_HOME="${JAVA_HOME:-/usr/lib/jvm/java-21-openjdk-amd64}"
export GRADLE_USER_HOME="${GRADLE_USER_HOME:-$HOME/.gradle}"
export PATH="$JAVA_HOME/bin:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools:$PATH"

echo "JAVA_HOME=$JAVA_HOME"
java -version
bash "$APP/scripts/prepare-www.sh"
cd "$APP"
npm install
npx cap sync android
cd "$APP/android"
chmod +x gradlew
./gradlew assembleDebug --no-daemon -Dorg.gradle.daemon=false

APK="$APP/android/app/build/outputs/apk/debug/app-debug.apk"
ls -lh "$APK"
echo "APK built: $APK"
