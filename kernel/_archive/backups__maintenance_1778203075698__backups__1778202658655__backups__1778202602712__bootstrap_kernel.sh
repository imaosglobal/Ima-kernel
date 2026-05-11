#!/data/data/com.termux/files/usr/bin/bash

echo "=== IMA KERNEL BOOTSTRAP START ==="

cd "$(dirname "$0")"

# 1. kill old node processes
echo "[1/5] Killing old node processes..."
pkill -f node || true

# 2. clean install npm
echo "[2/5] Installing dependencies..."
npm install

# 3. ensure env exists
echo "[3/5] Checking env..."
if [ ! -f .env ]; then
  echo "WARNING: .env missing"
fi

# 4. git sync (safe)
echo "[4/5] Git sync..."
git add .
git commit -m "kernel auto sync" || true
git push || true

# 5. start kernel
echo "[5/5] Starting kernel..."
PORT=4000 node ima_saas_full.js

