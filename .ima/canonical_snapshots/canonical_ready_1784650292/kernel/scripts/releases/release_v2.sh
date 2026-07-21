#!/bin/bash
set -e

echo "=== IMA RELEASE ENGINE v2 ==="

TS=$(date +%s)
SNAP="releases/snapshots/$TS"

mkdir -p "$SNAP"

echo "[1] PRECHECK"

# process check
pgrep -f ENTRYPOINT > /dev/null || { echo "NO ENTRYPOINT"; exit 1; }

# state check
STATE=$(node -e "console.log(JSON.stringify(require('./runtime/KERNEL_STATE').getState()))")

echo "$STATE" | grep -q "alive" || { echo "STATE NOT HEALTHY"; exit 1; }

echo "[2] SNAPSHOT"
cp -r runtime "$SNAP/"
cp -r core "$SNAP/"
cp package.json "$SNAP/" 2>/dev/null || true
cp start.sh "$SNAP/" 2>/dev/null || true

echo "[3] GIT COMMIT"
git add -A
git commit -m "AUTO RELEASE $TS" || true

echo "[4] VERSION BUMP"
NEW=$(node -e "
const fs=require('fs');
const p=require('./package.json');
if(!p.version) p.version='1.0.0';
const v=p.version.split('.').map(Number);
v[2]++;
p.version=v.join('.');
fs.writeFileSync('package.json',JSON.stringify(p,null,2));
console.log(p.version);
")

echo "VERSION: $NEW"

echo "[5] TAG + PUSH"
git tag -f "v$NEW"
git push origin main
git push origin -f "v$NEW"

echo "[6] NPM SAFE PUBLISH"
npm publish --access public || echo "npm skipped"

echo "=== RELEASE SUCCESS v$NEW ==="
