#!/data/data/com.termux/files/usr/bin/bash

set -e

APP_DIR="$(pwd)"
APK_PATH="app/build/outputs/apk/debug/app-debug.apk"
OUT="$HOME/ima_debug.apk"

echo "[1] Cleaning Gradle"
./gradlew clean

echo "[2] Forcing dependency refresh + rebuild"
./gradlew assembleDebug --no-daemon --refresh-dependencies

echo "[3] Checking APK"
if [ ! -f "$APK_PATH" ]; then
  echo "[ERROR] APK not found"
  exit 1
fi

echo "[4] Copying APK to home"
cp "$APK_PATH" "$OUT"

echo "[5] Verifying"
ls -lh "$OUT"

echo "[DONE] APK ready at $OUT"
