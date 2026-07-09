#!/usr/bin/env bash

echo "[IMA PIPELINE CLEAN CORE]"
echo "=============================="

echo "[1] sanity"
node -e "const p=require('./package.json'); if(!p.version) throw new Error('bad'); console.log('[OK]',p.version);"

echo "[2] core check"
for f in bin/ima global_boot.js api_layer.js db_memory.js; do
  test -f "$f" || { echo "[FATAL] $f"; exit 1; }
done

echo "[3] pack"
T=$(npm pack --silent)
echo "[PACKED] $T"

echo "[4] verify"
tar -tf "$T" | grep -q "global_boot.js" && echo "[OK] verified"

echo "[5] runtime DRY ONLY"
node -e "
try {
  require('./global_boot.js');
  console.log('[RUNTIME OK - DRY]');
} catch(e) {
  console.log('[RUNTIME ERROR]', e.message);
}
"

# חשוב: אין publish פה יותר
echo "[DONE] pipeline finished safely"
