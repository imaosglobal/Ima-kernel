#!/usr/bin/env bash

source ./ima_mode_guard.sh release

set -e

echo "[IMA RELEASE] FULL DEPLOY"

echo "[1] backup"
bash ima_backup.sh 2>/dev/null || true

echo "[2] git commit + push"
git add .
git commit -m "release $(date +%s)"
git push

echo "[3] version bump"
npm version patch -m "release %s"

echo "[4] npm publish"
npm publish

echo "[5] future sync hooks"
echo "[OK] site/app/device sync placeholder"
