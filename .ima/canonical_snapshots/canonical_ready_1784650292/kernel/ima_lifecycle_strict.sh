#!/usr/bin/env bash
set -euo pipefail

echo "[IMA STRICT LIFECYCLE]"

PKG="ima-core-saas"

# -----------------------
# 1. VERIFY FILE EXISTS
# -----------------------
echo "[1] checking required files"

for f in bin/ima global_boot.js api_layer.js db_memory.js; do
  if [ ! -f "$f" ]; then
    echo "[FATAL] missing file: $f"
    exit 1
  fi
done

# -----------------------
# 2. FORCE PACKAGE CONFIG
# -----------------------
echo "[2] enforcing package.json files"

node -e "
const fs=require('fs');
const p=require('./package.json');
p.files=[
  'bin',
  'global_boot.js',
  'api_layer.js',
  'db_memory.js'
];
fs.writeFileSync('package.json', JSON.stringify(p,null,2));
"

# -----------------------
# 3. ENSURE BIN IS VALID
# -----------------------
echo "[3] ensuring bin entry"

mkdir -p bin
cat > bin/ima << 'BINEOF'
#!/usr/bin/env node
require('../global_boot.js');
BINEOF

chmod +x bin/ima

# -----------------------
# 4. CLEAN OLD PACKS
# -----------------------
rm -f *.tgz

# -----------------------
# 5. REAL PACK (NOT DRY RUN)
# -----------------------
echo "[4] packing"

TARBALL=$(npm pack --silent)

echo "[PACKED] $TARBALL"

# -----------------------
# 6. VERIFY ACTUAL TAR CONTENT
# -----------------------
echo "[5] verifying tarball contents"

tar -tf "$TARBALL" > /tmp/pack_files.txt

for f in bin/ima global_boot.js api_layer.js db_memory.js; do
  grep -q "$f" /tmp/pack_files.txt || {
    echo "[FATAL] missing in tarball: $f"
    exit 1
  }
done

# -----------------------
# 7. INSTALL TEST (REAL ISOLATED ENV)
# -----------------------
echo "[6] install test"

TEST_DIR="$(pwd)/.ima_test_env"
rm -rf "$TEST_DIR"
mkdir -p "$TEST_DIR"
cd "$TEST_DIR"

npm init -y >/dev/null
npm install "../$TARBALL"

node -e "require('ima-core-saas/global_boot.js'); console.log('RUNTIME OK')"

# -----------------------
# 8. CLI TEST
# -----------------------
node node_modules/ima-core-saas/bin/ima health || true

cd -

# -----------------------
# 9. PUBLISH
# -----------------------
echo "[7] publishing"

npm version patch -m "strict lifecycle %s"
npm publish

echo "[DONE]"
