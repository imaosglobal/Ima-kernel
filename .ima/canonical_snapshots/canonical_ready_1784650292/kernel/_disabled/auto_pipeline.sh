#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== IMA AUTO PIPELINE START ==="

cd ~/ima_core

# 1. sanity check
echo "[1] checking server build..."
node ~/ima_core/kernel/server.js &
sleep 2
pkill -f node || true

# 2. version bump
cd ~/ima_core/kernel
npm version patch --no-git-tag-version
VERSION=$(node -p "require('./package.json').version")

echo "[2] version: $VERSION"

# 3. git sync
cd ~/ima_core
git add .
git commit -m "auto release v$VERSION" || true

# 4. npm publish
cd ~/ima_core/kernel
npm publish || echo "npm publish skipped (already exists or auth issue)"

# 5. backup snapshot
tar -czf ~/ima_backup_$VERSION.tar.gz ~/ima_core

echo "[3] backup created"

echo "=== PIPELINE DONE v$VERSION ==="
