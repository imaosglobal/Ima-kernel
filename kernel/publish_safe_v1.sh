#!/data/data/com.termux/files/usr/bin/bash

set -e

ROOT="$HOME/ima_core/kernel"
cd "$ROOT"

echo "[PIPE] safe publish v1 starting..."

echo "[CHECK] package sanity..."
node -p "require('./package.json').version" >/dev/null
node -p "require('./package.json').bin" >/dev/null
npm ls --depth=0 >/dev/null

echo "[OK] package valid"

echo "[CHECK] npm pack dry-run..."
PACK_OUTPUT=$(npm pack --dry-run)

echo "$PACK_OUTPUT" | grep "bin/ima" >/dev/null || {
  echo "[ERROR] bin missing in tarball"
  exit 1
}

echo "[OK] tarball valid"

echo "[CHECK] port 4000..."
if lsof -i :4000 >/dev/null 2>&1; then
  echo "[WARN] port in use → killing node"
  pkill -f node || true
  sleep 1
fi

echo "[OK] port free"

echo "[CHECK] CLI health..."
timeout 5 node bin/ima health || {
  echo "[FAIL] CLI health failed"
  echo "{\"error\":\"cli_health_failed\",\"time\":\"$(date -Iseconds)\"}" >> ima_memory.json
  exit 1
}

echo "[OK] CLI healthy"

echo "[LEARN] snapshot..."
echo "{\"time\":\"$(date -Iseconds)\",\"status\":\"pre_publish_ok\"}" >> ima_memory.json

echo "[VERSION] bumping..."
npm version patch -m "release(safe): validated pipeline"

echo "[PUBLISH] publishing..."
npm publish

echo "[DONE] published successfully"
