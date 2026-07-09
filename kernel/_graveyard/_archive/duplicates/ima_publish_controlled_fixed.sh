#!/usr/bin/env bash
set -euo pipefail

echo "[IMA CONTROLLED RELEASE]"

ROOT="$PWD"

# sanity
node -e "const p=require('./package.json'); console.log(p.name, p.version);"

# run pipeline
bash ima_run.sh

# verify success
if ! grep -q "state=SUCCESS" ima_runtime.log; then
  echo "[BLOCK] pipeline failed"
  exit 1
fi

echo "[OK] pipeline success"

# direct publish (no duplicate approval layer)
npm publish

echo "[DONE]"
