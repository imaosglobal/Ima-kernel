#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== KERNEL OS MODE BOOT ==="

cd ~/ima_core/kernel

echo "[1] Loading lock..."
node -e "console.log(require('./kernel_guard').validateKernel())"

echo "[2] Loading env..."
export $(cat ~/.env | grep -v '^#' | xargs)

echo "[3] Git safe state..."
git checkout main || true
git add -A
git commit -m "os mode auto sync" || true

echo "[4] Sync..."
git push origin main || true

echo "[5] Start kernel..."
node ima_saas_full.js

echo "=== OS MODE ACTIVE ==="
