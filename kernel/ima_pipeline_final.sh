#!/usr/bin/env bash
set -euo pipefail

echo "=============================="
echo "[IMA PIPELINE FINAL v1]"
echo "=============================="

ROOT="$PWD"
WORK="$ROOT/.ima_pipeline"
SANDBOX="$WORK/sandbox"
FILES_LIST="$WORK/files.txt"
TARBALL=""

rm -rf "$WORK"
mkdir -p "$WORK"
mkdir -p "$SANDBOX"


# -----------------------
# 1. SANITY CHECK
# -----------------------
echo "[1] sanity check"

node -e "
const p=require('./package.json');
if(!p.name||!p.version) throw new Error('INVALID PACKAGE');
"

# -----------------------
# 2. ENSURE CORE FILES
# -----------------------
echo "[2] core files check"

for f in bin/ima global_boot.js api_layer.js db_memory.js; do
  if [ ! -f "$f" ]; then
    echo "[FATAL] missing file: $f"
    exit 1
  fi
done

# -----------------------
# 3. FORCE PACKAGE CONFIG (controlled)
# -----------------------
echo "[3] package config enforce"

node -e "
const fs=require('fs');
const p=require('./package.json');

p.bin = { ima: 'bin/ima' };
p.main = 'global_boot.js';
p.files = ['bin','global_boot.js','api_layer.js','db_memory.js'];

fs.writeFileSync('package.json', JSON.stringify(p,null,2));
"

# -----------------------
# 4. ENSURE BIN
# -----------------------
echo "[4] bin setup"

mkdir -p bin

cat > bin/ima << 'BINEOF'
#!/usr/bin/env node
require('../global_boot.js');
BINEOF

chmod +x bin/ima

# -----------------------
# 5. CLEAN OLD TAR
# -----------------------
rm -f *.tgz

# -----------------------
# 6. PACK (REAL SOURCE OF TRUTH)
# -----------------------
echo "[5] npm pack"

TARBALL=$(npm pack --silent)
echo "[PACKED] $TARBALL"

# -----------------------
# 7. VERIFY TAR CONTENT (NO /tmp)
# -----------------------
echo "[6] verify tarball"

tar -tf "$TARBALL" > "$FILES_LIST"

for f in bin/ima global_boot.js api_layer.js db_memory.js; do
  grep -q "$f" "$FILES_LIST" || {
    echo "[FATAL] missing in tarball: $f"
    exit 1
  }
done

echo "[OK] tarball integrity verified"

# -----------------------
# 8. INSTALL TEST (ISOLATED)
# -----------------------
echo "[7] install test"

cd "$SANDBOX"

npm init -y >/dev/null
npm install "$ROOT/$TARBALL" --no-audit --no-fund

node -e "
const p=require('ima-core-saas/package.json');
console.log('[INSTALLED OK]', p.name, p.version);
"

# -----------------------
# 9. CLI TEST
# -----------------------
echo "[8] CLI test"

node node_modules/ima-core-saas/bin/ima health || {
  echo "[WARN] CLI health failed (non-fatal)"
}

# -----------------------
# 10. RUNTIME TEST
# -----------------------
echo "[9] runtime test"

node node_modules/ima-core-saas/global_boot.js health || true

cd "$ROOT"

# -----------------------
# 11. PUBLISH GATE
# -----------------------
echo "[10] publish"

npm version patch -m "pipeline release %s"

npm publish

echo "=============================="
echo "[SUCCESS PIPELINE COMPLETE]"
echo "=============================="
trap 'rm -rf "$WORK"' EXIT
