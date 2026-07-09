#!/usr/bin/env bash

set -e

echo "[IMA UPDATE v3]"

echo "[1] git pull"
git pull

echo "[2] install deps"
npm install --no-audit --no-fund

echo "[3] runtime test (SAFE ONLY)"
IMA_SAFE_MODE=1 node -e "require('./global_boot.js')"

echo "[OK] update complete (NO RUNTIME TOUCH)"
