#!/data/data/com.termux/files/usr/bin/bash

cd ~/ima_core/kernel

DATE=$(date +%F)
TIME=$(date +%T)

# current version
if [ ! -f VERSION ]; then
  echo "1.0.0" > VERSION
fi

OLD=$(cat VERSION)

# auto bump minor version
IFS='.' read -r MAJOR MINOR PATCH <<< "$OLD"
PATCH=$((PATCH+1))
NEW="$MAJOR.$MINOR.$PATCH"

echo $NEW > VERSION

echo "VERSION UPDATED: $OLD → $NEW"

# sync npm
npm version $NEW --no-git-tag-version >/dev/null 2>&1

# git release
git add .
git commit -m "release $NEW ($DATE $TIME)" >/dev/null 2>&1
git tag "v$NEW" >/dev/null 2>&1
git push origin main --tags >/dev/null 2>&1

echo "RELEASE DONE: $NEW"
