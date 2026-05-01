#!/usr/bin/env bash

set -e

echo "[IMA RELEASE v4 SAFE]"

# 1. backup
mkdir -p backups
tar -czf backups/backup_$(date +%s).tgz runtime pipeline 2>/dev/null || true

# 2. git
git add .
git commit -m "release $(date +%s)" || true
git push || true

# 3. version check (CRITICAL FIX)
CURRENT=$(node -e "console.log(require('./package.json').version)")
echo "[CURRENT VERSION] $CURRENT"

npm version patch -m "release %s"

NEW=$(node -e "console.log(require('./package.json').version)")
echo "[NEW VERSION] $NEW"

# 4. guard against duplicate publish
PUBLISHED=$(npm view ima-core-saas version 2>/dev/null || echo "none")

echo "[PUBLISHED VERSION] $PUBLISHED"

if [ "$NEW" = "$PUBLISHED" ]; then
  echo "[BLOCKED] version already published"
  exit 0
fi

# 5. publish
npm publish

echo "[OK] RELEASE DONE"
