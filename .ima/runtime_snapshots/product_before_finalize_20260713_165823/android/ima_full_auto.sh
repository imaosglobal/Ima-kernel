#!/usr/bin/env bash
set -e

echo "[IMA] 1. CLEAN + BUILD"
cd ~/ima_kernel/android
./gradlew clean assembleDebug --no-daemon

echo "[IMA] 2. FIND APK"
APK=$(find ~/ima_kernel/android -name "app-debug.apk" | grep "outputs/apk/debug" | head -n 1)

[ -f "$APK" ] || { echo "[IMA] ERROR: APK not found"; exit 1; }

echo "[IMA] APK: $APK"

echo "[IMA] 3. VERIFY METADATA"
PKG=$(aapt dump badging "$APK" | grep "package:" | cut -d"'" -f2)
LAUNCH=$(aapt dump badging "$APK" | grep launchable-activity | cut -d"'" -f2)

echo "[IMA] PACKAGE: $PKG"
echo "[IMA] LAUNCH: $LAUNCH"

[ "$PKG" = "com.ima.core" ] || { echo "[IMA] PACKAGE FAIL"; exit 1; }
[ "$LAUNCH" = "com.ima.core.MainActivity" ] || { echo "[IMA] LAUNCH FAIL"; exit 1; }

echo "[IMA] 4. COPY TO DOWNLOAD"
cp "$APK" /sdcard/Download/ima.apk

echo "[IMA] 5. OPEN INSTALLER"
termux-open /sdcard/Download/ima.apk || am start \
  -a android.intent.action.VIEW \
  -d "file:///sdcard/Download/ima.apk" \
  -t application/vnd.android.package-archive || true

echo "[IMA] 6. VERIFY INSTALL"
sleep 5

pm list packages | grep com.ima.core && echo "[IMA] INSTALLED OK" || echo "[IMA] NOT INSTALLED"

echo "[IMA] DONE"
