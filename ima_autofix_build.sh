#!/data/data/com.termux/files/usr/bin/bash
set -e

ROOT="$(cd "$(dirname "$0")" && pwd)"
APP="$ROOT/android"
SDK="$HOME/Android/Sdk"

echo "[IMA] START AUTO BUILD SYSTEM"

if [ ! -d "$APP" ]; then
  echo "[IMA][ERROR] Android project missing: $APP"
  exit 1
fi

if ! command -v java >/dev/null 2>&1; then
  pkg install -y openjdk-17
fi

export ANDROID_HOME="$SDK"
export PATH="$ANDROID_HOME/platform-tools:$PATH"

if [ ! -d "$SDK" ]; then
  echo "[IMA][ERROR] Android SDK missing: $SDK"
  exit 1
fi

cd "$APP"

if [ ! -f "./gradlew" ]; then
  echo "[IMA][ERROR] gradlew missing"
  exit 1
fi

chmod +x ./gradlew

cat > gradle.properties <<'EOF'
org.gradle.jvmargs=-Xmx2g -Dfile.encoding=UTF-8
org.gradle.daemon=false
android.useAndroidX=true
android.enableJetifier=true
EOF

cat > local.properties <<EOF
sdk.dir=$SDK
EOF

echo "[IMA] BUILD"
./gradlew clean assembleDebug --no-daemon

echo "[IMA] BUILD SUCCESS"
