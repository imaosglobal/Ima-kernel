#!/usr/bin/env bash
set -euo pipefail

echo "== SECRET SCAN =="

patterns='(BEGIN .* PRIVATE KEY|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{20,}|password[[:space:]]*[:=]|api[_-]?key[[:space:]]*[:=])'

if grep -RInE \
  --exclude-dir=.git \
  --exclude='*.pyc' \
  --exclude='*.glb' \
  --exclude='*.lock' \
  "$patterns" .; then
  echo "SECRET_SCAN=FAIL"
  exit 1
fi

echo "SECRET_SCAN=PASS"
