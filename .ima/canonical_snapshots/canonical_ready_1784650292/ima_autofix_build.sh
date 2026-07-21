#!/data/data/com.termux/files/usr/bin/bash
set -e

APP="$HOME/ima_kernel/android"
SDK="$HOME/Android/Sdk"

echo "[IMA] START AUTO BUILD SYSTEM"

# ------------------------
# Java
# ------------------------
if ! command -v java >/dev/null 2>&1; then
  pkg install -y openjdk-17
fi

# ------------------------
# SDK
# ------------------------
export ANDROID_HOME="$SDK"
export PATH="$ANDROID_HOME/platform-tools:$PATH"

if [ ! -d "$SDK" ]; then
  pkg install -y android-tools
fi

# ------------------------
# AAPT2 FIX (CRITICAL)
# ------------------------
if ! command -v aapt2 >/dev/null 2>&1; then
  pkg install -y aapt2
fi

AAPT2_BIN="$(which aapt2)"
echo "android.aapt2FromMavenOverride=$AAPT2_BIN" >> "$APP/gradle.properties" || true

# ------------------------
# Gradle wrapper
# ------------------------
cd "$APP"

if [ ! -f "./gradlew" ]; then
  gradle wrapper
fi

chmod +x ./gradlew

# ------------------------
# local.properties fix
# ------------------------
cat > local.properties <<EOF2
sdk.dir=$SDK
EOF2

# ------------------------
# cache cleanup (safe)
# ------------------------
rm -rf ~/.gradle/caches/transforms-4 || true
rm -rf ~/.gradle/caches/*aapt2* || true

# ------------------------
# build loop
# ------------------------
TRIES=0
MAX=3

while [ $TRIES -lt $MAX ]
do
  TRIES=$((TRIES+1))

  echo "[IMA] BUILD TRY $TRIES"

  if ./gradlew clean assembleDebug --no-daemon; then
    echo "[IMA] SUCCESS"
    exit 0
  fi

  echo "[IMA] FAILED -> repairing"
  rm -rf ~/.gradle/caches/transforms-4 || true
  rm -rf ~/.gradle/caches/*aapt2* || true
  sleep 2
done

echo "[IMA] FINAL FAILURE"
exit 1
