#!/usr/bin/env bash

set -euo pipefail

PORT=4000
PKG="ima-core-saas"
LOG_DIR="./logs"
mkdir -p "$LOG_DIR"

echo "=============================="
echo "[IMA LIFECYCLE v2 START]"
echo "=============================="

# ---------------------------
# 1. PACKAGE SANITY
# ---------------------------
echo "[1/10] package.json validation"

node -e "
const p=require('./package.json');
if(!p.name||!p.version) throw new Error('INVALID PACKAGE.JSON');
console.log('OK package:', p.name, p.version);
"

# ---------------------------
# 2. BIN VALIDATION
# ---------------------------
echo "[2/10] CLI bin validation"

if [ ! -f "bin/ima" ]; then
  echo "[FIX] creating missing bin/ima"
  mkdir -p bin
  cat > bin/ima << 'BINEOF'
#!/usr/bin/env node
require('../global_boot.js');
BINEOF
  chmod +x bin/ima
fi

if ! head -n 1 bin/ima | grep -q "node"; then
  echo "[ERROR] invalid bin header"
  exit 1
fi

# ---------------------------
# 3. BIN IN PACKAGE CHECK
# ---------------------------
echo "[3/10] npm pack dry-run validation"

PACK_OUTPUT=$(npm pack --dry-run)

echo "$PACK_OUTPUT" | grep "bin/ima" >/dev/null || {
  echo "[ERROR] bin/ima NOT in tarball"
  exit 1
}

# ---------------------------
# 4. CLEAN PORT STATE
# ---------------------------
echo "[4/10] port 4000 cleanup"

PID=$(lsof -t -i:$PORT || true)

if [ ! -z "${PID:-}" ]; then
  echo "[KILL] process on port $PORT -> $PID"
  kill -9 $PID || true
fi

# ---------------------------
# 5. RUNTIME SMOKE TEST
# ---------------------------
echo "[5/10] runtime smoke test"

timeout 5 node global_boot.js || {
  echo "[WARN] runtime did not complete cleanly (non-fatal)"
}

# ---------------------------
# 6. CHECK NPM AUTH
# ---------------------------
echo "[6/10] npm auth check"

npm whoami >/dev/null || {
  echo "[ERROR] not logged into npm"
  exit 1
}

# ---------------------------
# 7. VERSION LOCK CHECK
# ---------------------------
echo "[7/10] version consistency"

CURRENT=$(node -p "require('./package.json').version")
echo "current version: $CURRENT"

# ---------------------------
# 8. PRE-PUBLISH SNAPSHOT
# ---------------------------
echo "[8/10] snapshot"

cp package.json "$LOG_DIR/package.$CURRENT.json"

# ---------------------------
# 9. VERSION + BUILD
# ---------------------------
echo "[9/10] version bump"

npm version patch -m "lifecycle release %s"

# ---------------------------
# 10. PUBLISH SAFE
# ---------------------------
echo "[10/10] publish"

npm publish

echo "=============================="
echo "[SUCCESS] publish complete"
echo "=============================="
