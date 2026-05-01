#!/usr/bin/env bash
set -e

echo "[IMA UPDATE SAFE]"
echo "================"

echo "[1] git sync (pull only)"
git pull --rebase || true

echo "[2] install deps"
npm install --no-audit --no-fund

echo "[3] sanity check"
node -e "const p=require('./package.json'); console.log('[OK]',p.version)"

echo "[4] runtime dry check"
node -e "require('./global_boot.js'); console.log('[OK] runtime loaded')"

echo "================"
echo "[UPDATE DONE - NO RELEASE]"
