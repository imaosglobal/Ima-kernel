#!/data/data/com.termux/files/usr/bin/bash

cd ~/ima_core/kernel

CURRENT=$(cat VERSION)
NPM_VER=$(node -p "require('./package.json').version")

echo "LOCAL VERSION FILE: $CURRENT"
echo "NPM VERSION: $NPM_VER"

if [ "$CURRENT" != "$NPM_VER" ]; then
  echo "⚠ VERSION MISMATCH → syncing npm to file"
  sed -i "s/\"version\": \".*\"/\"version\": \"$CURRENT\"/" package.json
  git add package.json VERSION
  git commit -m "sync version $CURRENT"
  git push origin main
else
  echo "✔ VERSION OK"
fi
