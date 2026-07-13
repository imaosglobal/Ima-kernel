#!/usr/bin/env bash
set -e

echo "[IMA] BUILD START"

cd ~/ima_kernel/android
./gradlew clean assembleDebug --no-daemon

APK=$(find app/build/outputs/apk/debug -name "*.apk" | head -n 1)

echo "[IMA] APK: $APK"

[ -f "$APK" ] || { echo "[IMA] ERROR: APK missing"; exit 1; }

DEST="/sdcard/Download/ima_debug.apk"

cp "$APK" "$DEST"

echo "[IMA] OPENING SYSTEM INSTALLER"

# הדרך הכי יציבה באנדרואיד מודרני
am start \
  -a android.intent.action.VIEW \
  -d "content://com.android.externalstorage.documents/document/primary:Download/ima_debug.apk" \
  -t application/vnd.android.package-archive || \
termux-open "$DEST" || true

echo "[IMA] WAITING FOR INSTALL..."
sleep 10

echo "[IMA] VERIFY PACKAGE"
pm list packages | grep com.ima.core || echo "[IMA] NOT INSTALLED"

echo "[IMA] DONE"
