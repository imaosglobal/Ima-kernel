#!/usr/bin/env bash

echo "[GATE] pre-publish validation..."

# 1. בדיקת bin קיים
if [ ! -f bin/ima ]; then
  echo "[ERROR] bin/ima missing"
  exit 1
fi

# 2. בדיקת executable
if [ ! -x bin/ima ]; then
  echo "[ERROR] bin/ima not executable"
  exit 1
fi

# 3. בדיקת package.json bin mapping
node -e "const p=require('./package.json'); if(!p.bin || !p.bin.ima){process.exit(1)}"

if [ $? -ne 0 ]; then
  echo "[ERROR] bin mapping invalid"
  exit 1
fi

# 4. בדיקת tarball preview
npm pack --dry-run | grep "bin/ima" >/dev/null

if [ $? -ne 0 ]; then
  echo "[ERROR] bin not included in tarball"
  exit 1
fi

echo "[GATE] OK"
