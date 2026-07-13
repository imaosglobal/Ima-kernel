#!/usr/bin/env bash
set -e

echo "[IMA] STEP 1 - BUILD"
./gradlew clean assembleDebug --no-daemon

APK=$(find app/build/outputs/apk/debug -name "*.apk" | head -n 1)

echo "[IMA] APK FOUND: $APK"

[ -f "$APK" ] || { echo "[IMA] ERROR: APK missing"; exit 1; }

echo "[IMA] STEP 2 - COPY LOCAL"
cp "$APK" ~/ima_debug.apk

DEST="/sdcard/Download/ima_debug.apk"

echo "[IMA] STEP 3 - COPY TO DOWNLOAD"
cp ~/ima_debug.apk "$DEST"

echo "[IMA] STEP 4 - VERIFY"
ls -lh "$DEST"

echo "[IMA] STEP 5 - OPEN INSTALLER (ANDROID INTENT)"
am start \
  -a android.intent.action.VIEW \
  -d "file://$DEST" \
  -t application/vnd.android.package-archive || true

echo "[IMA] STEP 6 - CHECK INSTALL"
sleep 5

pm list packages | grep com.ima.core || echo "[IMA] NOT INSTALLED YET"

echo "[IMA] DONE"
