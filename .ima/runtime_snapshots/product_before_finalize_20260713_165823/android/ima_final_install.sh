#!/usr/bin/env bash
set -e

echo "[IMA] BUILD"
cd ~/ima_kernel/android
./gradlew clean assembleDebug --no-daemon

APK=$(find app/build/outputs/apk/debug -name "*.apk" | head -n 1)

echo "[IMA] APK: $APK"

DEST="/sdcard/Download/ima_debug.apk"
cp "$APK" "$DEST"

echo "[IMA] OPEN SYSTEM INSTALLER"

am start \
-a android.intent.action.INSTALL_PACKAGE \
-d "file:///sdcard/Download/ima_debug.apk" || \
am start \
-a android.intent.action.VIEW \
-d "file:///sdcard/Download/ima_debug.apk" \
-t application/vnd.android.package-archive

echo "[IMA] WAIT FOR USER INSTALL"
sleep 15

echo "[IMA] VERIFY"
pm list packages | grep com.ima.core || echo "[IMA] NOT INSTALLED"

