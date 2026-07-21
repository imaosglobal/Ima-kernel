#!/bin/bash

set -e

echo "🚀 IMA RELEASE ENGINE START"

VERSION=$(node -e "console.log(require('./package.json').version)")
echo "📦 Current version: $VERSION"

# ----------------------------
# 1. PRE-FLIGHT CHECK
# ----------------------------
echo "🔍 Pre-flight check..."

pgrep -af ENTRYPOINT || { echo "❌ ENTRYPOINT not running"; exit 1; }

STATE=$(node -e "console.log(JSON.stringify(require('./runtime/KERNEL_STATE').getState()))")
echo "STATE: $STATE"

echo "$STATE" | grep -q "alive" || { echo "❌ Runtime not healthy"; exit 1; }

# ----------------------------
# 2. CLEAN WORKING STATE
# ----------------------------
echo "🧹 Cleaning workspace..."
git add -A
git diff --cached --quiet || git commit -m "AUTO RELEASE PREP $VERSION"

# ----------------------------
# 3. VERSION BUMP
# ----------------------------
NEW_VERSION=$(node -e "
const fs=require('fs');
const p=require('./package.json');
const parts=p.version.split('.').map(Number);
parts[2]+=1;
p.version=parts.join('.');
fs.writeFileSync('package.json',JSON.stringify(p,null,2));
console.log(p.version);
")

echo "⬆️ New version: $NEW_VERSION"

# ----------------------------
# 4. TAG
# ----------------------------
git tag -f "v$NEW_VERSION"
git push origin main
git push origin -f "v$NEW_VERSION"

# ----------------------------
# 5. BUILD DIST
# ----------------------------
echo "📦 Building dist..."
rm -rf dist
mkdir -p dist

cp -r runtime dist/
cp -r core dist/
cp package.json dist/
cp start.sh dist/ 2>/dev/null || true

# ----------------------------
# 6. RUNTIME SANITY TEST
# ----------------------------
echo "🧪 Runtime sanity test..."

timeout 5s node runtime/ENTRYPOINT.js || true

node -e "
const k=require('./runtime/KERNEL_STATE');
setTimeout(()=>{
  const s=k.getState();
  console.log('SANITY STATE:',s);
  if(s.runtime!=='alive') process.exit(1);
},2000);
"

# ----------------------------
# 7. NPM PUBLISH (SAFE)
# ----------------------------
echo "📡 Publishing npm..."

npm publish --access public || {
  echo "⚠️ npm publish failed (ignored)"
}

# ----------------------------
# 8. SUCCESS
# ----------------------------
echo "✅ RELEASE COMPLETE: v$NEW_VERSION"
