#!/usr/bin/env bash
set -e

echo "[IMA] 1. BUILDING..."
cd ~/ima_kernel/android
./gradlew clean assembleDebug --no-daemon

APK=$(find app/build/outputs/apk/debug -name "*.apk" | head -n 1)

# העתקה לנפח משותף גלובלי
DEST="/sdcard/Download/ima_debug.apk"
cp "$APK" "$DEST"

echo "[IMA] 2. OPENING WITH SYSTEM PROVIDER..."
# טרמוקס מתרגם ישירות את termux-open ל-Content URI מוגן
termux-open "$DEST"

echo "[IMA] WAITING FOR INSTALLATION..."
sleep 15

if pm list packages | grep -q "com.ima.core"; then
    echo "[IMA] SUCCESS: INSTALLED!"
    am start -n "com.ima.core/com.ima.core.MainActivity"
else
    echo "[IMA] FAILED TO DETECT PACKAGE."
fi
