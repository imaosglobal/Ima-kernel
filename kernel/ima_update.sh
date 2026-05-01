#!/data/data/com.termux/files/usr/bin/bash

cd ~/ima_core/kernel

echo "[IMA UPDATE SYNC]"

# ===== PULL =====
echo "[SYNC] pulling from git..."
git pull origin main || true

# ===== INSTALL =====
echo "[SYNC] installing deps..."
npm install || true

# ===== ADD ONLY SAFE FILES =====
echo "[SYNC] staging changes..."

git add *.js 2>/dev/null
git add *.sh 2>/dev/null
git add package.json 2>/dev/null

# ===== COMMIT IF CHANGES =====
if ! git diff --cached --quiet; then
  echo "[SYNC] committing..."
  git commit -m "auto sync $(date)"
  
  echo "[SYNC] pushing..."
  git push origin main
else
  echo "[SYNC] no code changes to push"
fi

# ===== RESTART =====
echo "[SYNC] restarting..."
bash ~/ima_core/kernel/ima_restart.sh

echo "[IMA UPDATE SYNC DONE]"
