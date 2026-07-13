#!/usr/bin/env bash

set -e

echo "[IMA] BUILD START"

./gradlew clean assembleDebug --no-daemon

APK_SRC=$(find app/build/outputs/apk/debug -name "*.apk" | head -n 1)

if [ -z "$APK_SRC" ]; then
  echo "[IMA] APK NOT FOUND"
  exit 1
fi

echo "[IMA] APK FOUND: $APK_SRC"

cp "$APK_SRC" ~/ima_debug.apk

echo "[IMA] COPIED TO HOME"

DEST="/sdcard/Download/ima_debug.apk"

cp ~/ima_debug.apk "$DEST"

echo "[IMA] COPIED TO DOWNLOAD: $DEST"

# פתיחה דרך Android Installer
termux-open "$DEST" || true

echo "[IMA] OPEN INSTALLER SENT"

echo "[IMA] DONE"
