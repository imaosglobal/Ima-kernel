#!/usr/bin/env bash
set -e

echo "[IMA] STEP 1 - CLEAN BUILD"
./gradlew clean assembleDebug --no-daemon

APK=$(find app/build/outputs/apk/debug -name "*.apk" | head -n 1)

echo "[IMA] STEP 2 - VERIFY APK EXISTS"
[ -f "$APK" ] || { echo "[IMA] BUILD FAILED - APK missing"; exit 1; }

echo "[IMA] STEP 3 - VERIFY PACKAGE"
PKG=$(aapt dump badging "$APK" | grep "package: name" | cut -d"'" -f2)

echo "[IMA] PACKAGE: $PKG"

[ "$PKG" = "com.ima.core" ] || {
  echo "[IMA] PACKAGE MISMATCH"
  exit 1
}

echo "[IMA] STEP 4 - VERIFY LAUNCHABLE"
LAUNCH=$(aapt dump badging "$APK" | grep launchable-activity | cut -d"'" -f2)

echo "[IMA] LAUNCH: $LAUNCH"

[ "$LAUNCH" = "com.ima.core.MainActivity" ] || {
  echo "[IMA] LAUNCH MISMATCH"
  exit 1
}

echo "[IMA] STEP 5 - COPY OUTPUT"
cp "$APK" ~/ima_debug.apk
cp ~/ima_debug.apk /sdcard/Download/ima_debug.apk || true

echo "[IMA] STEP 6 - OPEN INSTALLER"
am start -a android.intent.action.VIEW \
  -d "file:///sdcard/Download/ima_debug.apk" \
  -t application/vnd.android.package-archive || true

echo "[IMA] DONE - SYSTEM VALIDATED"
