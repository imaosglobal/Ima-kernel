#!/system/bin/sh
set -eu

ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
UI="$ROOT/ima-ui"
ANDROID="$ROOT/android/app/src/main/assets/ima-ui"

echo "[IMA] building shared web client"
cd "$UI"
npm ci
npm run build

echo "[IMA] synchronizing Android client"
rm -rf "$ANDROID"
mkdir -p "$ANDROID"
cp -R "$UI/dist/." "$ANDROID/"

test -s "$UI/dist/index.html"
test -s "$UI/dist/manifest.json"
test -s "$ANDROID/index.html"

if grep -R -n "mother_character.glb" "$UI/src" >/dev/null 2>&1; then
  echo "[IMA] source references verified"
fi

echo "[IMA] WEB_AND_ANDROID_SYNC=PASS"
echo "[IMA] next: build Android with Gradle"
