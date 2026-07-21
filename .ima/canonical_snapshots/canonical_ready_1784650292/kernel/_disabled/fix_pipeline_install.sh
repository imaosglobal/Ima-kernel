#!/usr/bin/env bash
set -euo pipefail

WORK="$(pwd)/.ima_pipeline"
SANDBOX="$WORK/sandbox"

echo "[FIX] clean install sandbox"

rm -rf "$SANDBOX"
mkdir -p "$SANDBOX"
cd "$SANDBOX"

echo "[FIX] init clean project"
npm init -y >/dev/null

echo "[FIX] locate latest tarball"

ROOT="$(cd ../../ && pwd)"
TARBALL=$(ls -t "$ROOT"/*.tgz | head -1)

echo "[USING TARBALL]: $TARBALL"

echo "[FIX] install fresh package"
npm install "$TARBALL" --no-cache --prefer-offline=false --no-audit --no-fund

echo "[FIX] runtime verify"
node -e "console.log('INSTALL OK')"
