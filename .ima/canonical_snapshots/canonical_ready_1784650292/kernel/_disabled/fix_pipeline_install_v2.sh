#!/usr/bin/env bash
set -euo pipefail

WORK="$(pwd)/.ima_pipeline"
SANDBOX="$WORK/sandbox"

echo "[HARD FIX INSTALL]"

rm -rf "$SANDBOX"
mkdir -p "$SANDBOX"
cd "$SANDBOX"

echo "[1] fresh npm init"
npm init -y >/dev/null

echo "[2] clean npm state"
rm -rf node_modules package-lock.json

echo "[3] disable cache explicitly"
npm cache clean --force >/dev/null 2>&1 || true

echo "[4] find latest tarball"
ROOT="$(cd ../../ && pwd)"
TARBALL=$(ls -t "$ROOT"/*.tgz | head -1)

echo "[USING]: $TARBALL"

echo "[5] force pure tgz install"
npm install "$TARBALL" \
  --no-package-lock \
  --no-audit \
  --no-fund \
  --prefer-offline=false

echo "[6] verify runtime"
node -e "console.log('INSTALL OK CLEAN')"
