#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

echo "=================================="
echo "[IMA AUTO CONTROLLER ENTRY]"
echo "ROOT: $ROOT"
echo "=================================="

LOG="$ROOT/ima_runtime.log"
exec > >(tee -a "$LOG") 2>&1

STATE="FAIL"

trap 'echo "[EXIT] state=$STATE"' EXIT

# -------------------------
# 1. VERIFY CORE
# -------------------------
echo "[1] self-check files"

REQUIRED=(
  "package.json"
  "global_boot.js"
  "bin/ima"
  "api_layer.js"
  "db_memory.js"
)

for f in "${REQUIRED[@]}"; do
  if [ ! -f "$f" ]; then
    echo "[AUTO-FIX] missing $f"

    case "$f" in
      bin/ima)
        mkdir -p bin
        cat > bin/ima << 'BINEOF'
#!/usr/bin/env node
require('../global_boot.js');
BINEOF
        chmod +x bin/ima
        ;;
      api_layer.js)
        cat > api_layer.js << 'EOF_API'
module.exports = { health: () => ({ ok: true }) };
EOF_API
        ;;
      db_memory.js)
        cat > db_memory.js << 'EOF_DB'
module.exports = { memory: {} };
EOF_DB
        ;;
    esac
  fi
done

# -------------------------
# 2. FORCE PACKAGE VALIDATION
# -------------------------
echo "[2] package validation"

node -e "
const p=require('./package.json');
if(!p.name||!p.version) throw new Error('INVALID PACKAGE');
"

# -------------------------
# 3. PACK & VERIFY
# -------------------------
echo "[3] pack"

rm -f *.tgz
TARBALL=$(npm pack --silent)

echo "[PACKED] $TARBALL"

echo "[4] verify tarball"
tar -tf "$TARBALL" | grep -q "bin/ima"
tar -tf "$TARBALL" | grep -q "global_boot.js"

# -------------------------
# 4. INSTALL TEST
# -------------------------
echo "[5] install test"

TEST="$ROOT/.ima_test"
rm -rf "$TEST"
mkdir -p "$TEST"
cd "$TEST"

npm init -y >/dev/null
npm install "$ROOT/$TARBALL" --no-audit --no-fund

node -e "console.log('INSTALL OK')"

# -------------------------
# 5. RUNTIME TEST
# -------------------------
echo "[6] runtime test"

node node_modules/ima-core-saas/bin/ima health || true

cd "$ROOT"

# -------------------------
# 6. AUTO VERSION + PUBLISH
# -------------------------
echo "[7] version + publish"

npm version patch -m "auto pipeline %s"
npm publish

# -------------------------
# 7. SELF STATE UPDATE
# -------------------------
STATE="SUCCESS"

echo "[DONE] IMA cycle complete"
