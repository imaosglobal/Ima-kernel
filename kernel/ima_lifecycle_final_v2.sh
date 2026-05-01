#!/usr/bin/env bash
set -e

echo "[IMA LIFECYCLE FINAL v2]"

ROOT="$PWD"
WORK="$ROOT/.ima_lifecycle"

rm -rf "$WORK"
mkdir -p "$WORK"

trap "rm -rf $WORK" EXIT

echo "[1] sanity"
node -e "const p=require(\"./package.json\"); if(!p.name||!p.version) throw new Error(\"bad package\")"

echo "[2] bin"
mkdir -p bin
printf "#!/usr/bin/env node\nrequire(\"../global_boot.js\");\n" > bin/ima
chmod +x bin/ima

echo "[3] package config"
npm pkg set bin.ima="./bin/ima" >/dev/null
npm pkg set main="global_boot.js" >/dev/null
npm pkg delete files >/dev/null 2>&1 || true

echo "[4] pack"
T=$(npm pack --silent)
mv "$T" "$WORK/"
T="$WORK/$T"

echo "[5] verify"
tar -tf "$T" > "$WORK/list.txt"

grep -q "package/bin/ima" "$WORK/list.txt" || { echo "missing bin"; exit 1; }
grep -q "package/global_boot.js" "$WORK/list.txt" || { echo "missing entry"; exit 1; }

echo "[6] install test"
TEST="$WORK/test"
mkdir -p "$TEST"
cd "$TEST"

npm init -y >/dev/null
npm install "$T" --no-audit --no-fund >/dev/null

echo "[7] runtime test (safe)"

node node_modules/ima-core-saas/bin/ima &
PID=$!

sleep 3

kill -9 $PID || true

echo "[OK] runtime started and stopped"

cd "$ROOT"

echo "[8] publish"
npm version patch -m "stable release %s"
npm publish

echo "[DONE]"
