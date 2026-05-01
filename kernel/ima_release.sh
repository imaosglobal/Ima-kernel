#!/usr/bin/env bash
set -euo pipefail

echo "[IMA RELEASE]"

echo "[1] backup safety"
TS=$(date +%s)
mkdir -p backups
tar -czf backups/pre_release_$TS.tgz .

echo "[2] git commit + push"
git add .
git commit -m "release $(date +%s)" || true
git push

echo "[3] version bump"
node -e "
const fs=require('fs');
const p=require('./package.json');
let [a,b,c]=(p.version||'2.0.0').split('.');
p.version=\`\${a}.\${parseInt(b)+1}.0\`;
fs.writeFileSync('package.json',JSON.stringify(p,null,2));
console.log('[VERSION]',p.version);
"

echo "[4] npm publish"
npm publish

echo "[5] sync hooks (future: site/app)"
echo "[OK] release complete"
