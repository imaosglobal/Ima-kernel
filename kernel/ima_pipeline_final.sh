#!/usr/bin/env bash
set -euo pipefail

echo "=============================="
echo "[IMA PIPELINE STABLE]"
echo "=============================="

# 1. sanity
echo "[1] sanity check"
node -e "
const p=require('./package.json');
if(!p.name||!p.version) throw new Error('INVALID PACKAGE');
console.log('[OK]', p.version);
"

# 2. core files
echo "[2] core files check"
for f in bin/ima global_boot.js api_layer.js db_memory.js; do
  [ -f "$f" ] || { echo "[FATAL] missing $f"; exit 1; }
done
echo "[OK] files present"

# 3. enforce package.json
echo "[3] package config enforce"
node -e "
const fs=require('fs');
const p=require('./package.json');

p.bin={ima:'bin/ima'};
p.main='global_boot.js';
p.files=['bin','global_boot.js','api_layer.js','db_memory.js'];

fs.writeFileSync('package.json', JSON.stringify(p,null,2));
console.log('[OK] package fixed');
"

# 4. bin setup
echo "[4] bin setup"
mkdir -p bin
cat > bin/ima << 'BINEOF'
#!/usr/bin/env node
require('../global_boot.js');
BINEOF
chmod +x bin/ima

# 5. pack
echo "[5] npm pack"
rm -f *.tgz
TARBALL=$(npm pack --silent)
echo "[PACKED] $TARBALL"

# 6. verify
echo "[6] verify tarball"
tar -tf "$TARBALL" | grep -q "global_boot.js"
tar -tf "$TARBALL" | grep -q "bin/ima"
echo "[OK] tarball verified"

# 7. publish
echo "[7] publish"
npm version patch -m "stable pipeline %s"
npm publish

echo "=============================="
echo "[SUCCESS - DONE]"
echo "=============================="
