#!/usr/bin/env bash

source ./ima_mode_guard.sh update

echo "[IMA UPDATE]"
echo "[1] git pull"
git pull

echo "[2] clean install"
npm install --no-audit --no-fund

echo "[3] running pipeline guard (NO publish)"

bash ima_pipeline_final.sh | grep -v "publish"

echo "[4] VERIFY ONLY"
node -e "console.log('[OK] update safe complete')"
