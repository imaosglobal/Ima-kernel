#!/usr/bin/env bash

set -e

echo "[IMA RELEASE v3 FIXED]"

echo "[1] backup safe (only existing dirs)"

BACKUP_NAME="backups/backup_$(date +%s).tgz"
mkdir -p backups

tar -czf "$BACKUP_NAME" \
  runtime \
  pipeline \
  2>/dev/null || true

echo "[BACKUP CREATED] $BACKUP_NAME"

echo "[2] git commit"
git add .
git commit -m "release $(date +%s)" || true
git push || true

echo "[3] npm publish"
npm version patch -m "release %s"
npm publish

echo "[OK] RELEASE DONE"
