#!/usr/bin/env bash

set -e

ROOT="$(pwd)"
IMA="$ROOT/.ima"
ANDROID="$ROOT/android"

echo "[IMA] controller start"

# -------------------------
# 1. sanity checks
# -------------------------
if [ ! -d "$IMA" ]; then
  echo "[IMA][ERROR] missing .ima directory"
  exit 1
fi

if [ ! -d "$ANDROID" ]; then
  echo "[IMA][ERROR] missing android project"
  exit 1
fi

if [ ! -f "$ANDROID/gradlew" ]; then
  echo "[IMA][ERROR] missing gradlew"
  exit 1
fi

chmod +x "$ANDROID/gradlew"

# -------------------------
# 2. load state (if exists)
# -------------------------
STATE="$IMA/state.json"
GRAPH="$IMA/graph.json"

echo "[IMA] reading state"

if [ ! -f "$STATE" ]; then
  echo '{}' > "$STATE"
fi

if [ ! -f "$GRAPH" ]; then
  echo '{}' > "$GRAPH"
fi

# -------------------------
# 3. cleanup unstable caches
# -------------------------
echo "[IMA] cleaning caches"
rm -rf ~/.gradle/caches/transforms-* || true
rm -rf ~/.gradle/caches/modules-* || true
rm -rf "$ANDROID/.gradle" || true

# -------------------------
# 4. ensure SDK config
# -------------------------
if [ ! -f "$ANDROID/local.properties" ]; then
  echo "sdk.dir=$HOME/Android/Sdk" > "$ANDROID/local.properties"
fi

cat > "$ANDROID/gradle.properties" <<EOP
org.gradle.jvmargs=-Xmx2g -Dfile.encoding=UTF-8
org.gradle.daemon=false
android.useAndroidX=true
android.enableJetifier=true
android.aapt2FromMavenOverride=false
EOP

# -------------------------
# 5. run build
# -------------------------
echo "[IMA] building APK"

cd "$ANDROID"

if ./gradlew clean assembleDebug --no-daemon; then
  echo "[IMA] BUILD SUCCESS"

  echo '{"last_build":"success"}' > "$STATE"

else
  echo "[IMA] BUILD FAILED"

  echo '{"last_build":"failed"}' > "$STATE"

  # lightweight self-fix logic (safe minimal)
  echo "[IMA] attempting recovery cleanup"
  rm -rf ~/.gradle/caches/transforms-* || true
fi

# -------------------------
# 6. update graph snapshot (minimal placeholder)
# -------------------------
echo "{\"status\":\"updated\"}" > "$GRAPH"

echo "[IMA] controller done"
