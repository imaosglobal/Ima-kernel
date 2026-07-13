#!/usr/bin/env bash
set -e

echo "[IMA] BUILD"
cd ~/ima_kernel/android
./gradlew clean assembleDebug --no-daemon

APK=$(find app/build/outputs/apk/debug -name "*.apk" | head -n 1)

echo "[IMA] APK READY: $APK"

DEST="/sdcard/Download/ima_debug.apk"
cp "$APK" "$DEST"

echo "[IMA] OPENING DOWNLOADS (SAFE MODE)"

am start \
-a android.intent.action.VIEW \
-d "file:///sdcard/Download/ima_debug.apk" \
-t application/vnd.android.package-archive

echo "[IMA] PLEASE CONFIRM INSTALL MANUALLY"

sleep 10

echo "[IMA] VERIFY INSTALL"
pm list packages | grep com.ima.core || echo "[IMA] NOT INSTALLED"
