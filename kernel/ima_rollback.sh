#!/usr/bin/env bash
set -euo pipefail

BACKUP=$(cat ~/.ima_backups/ima_core/kernel/.ima_last_backup 2>/dev/null || cat .ima_last_backup)

if [ -z "$BACKUP" ]; then
  echo "[ROLLBACK FAILED] no backup found"
  exit 1
fi

echo "[ROLLBACK TO]: $BACKUP"

rm -rf .
cp -r ~/.ima_backups/$BACKUP/* .

echo "[ROLLBACK COMPLETE]"
