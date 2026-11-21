#!/usr/bin/env bash
# Prepare the Capacitor webDir from the live-site source of truth (final-deploy).
# DailyTools' root index.html IS the app (single-page app), so no redirect is
# needed — copy final-deploy as-is into www.
# Usage: bash android-app/scripts/prepare-www.sh   (run from the repo root)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
rm -rf "$ROOT/android-app/www"
mkdir -p "$ROOT/android-app/www"
cp -r "$ROOT/final-deploy/." "$ROOT/android-app/www/"
rm -f "$ROOT/android-app/www"/*.apk  # never bundle a previous APK inside the new one
echo "www prepared: $(find "$ROOT/android-app/www" -type f | wc -l) files"
