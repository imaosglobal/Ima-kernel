#!/usr/bin/env bash
set -euo pipefail

echo "[IMA UPDATE]"

echo "[1] git pull"
git pull

echo "[2] clean install"
rm -rf node_modules package-lock.json
npm install --no-audit --no-fund

echo "[3] run pipeline tests (NO publish)"
bash ima_pipeline_final.sh

echo "[OK] update complete"
