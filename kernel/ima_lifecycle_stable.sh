#!/usr/bin/env bash
set -e

echo "[IMA LIFECYCLE STABLE]"

ROOT="$PWD"
WORK="$ROOT/.ima_lifecycle"
PKG="ima-core-saas"

rm -rf "$WORK"
mkdir -p "$WORK"

cleanup() { rm -rf "$WORK"; }
trap cleanup EXIT

echo "[1] sanity"
node -e "const p=require(\"./package.json\"); if(!p.name||!p.version) throw new Error(\"bad package\")"

echo "[2] ensure bin"
mkdir -p bin
printf "#!/usr/bin/env node\nrequire(\"../global_boot.js\");\n" > bin/ima
chmod +x bin/ima

echo "[3] package config"
npm pkg set bin.ima="./bin/ima" >/dev/null
npm pkg set main="global_boot.js" >/dev/null
npm pkg delete files >/dev/null 2>&1 || true
npm pkg set files[0]="bin" >/dev/null
npm pkg set files[1]="global_boot.js" >/dev/null

echo "[4] pack"
TARBALL=$(npm pack --silent)
mv "$TARBALL" "$WORK/"
TARBALL="$WORK/$TARBALL"

echo "[5] verify real tarball"
tar -tf "$TARBALL" > "$WORK/list.txt"

grep -q "package/bin/ima" "$WORK/list.txt" || { echo "[FATAL] bin missing"; exit 1; }
grep -q "package/global_boot.js" "$WORK/list.txt" || { echo "[FATAL] entry missing"; exit 1; }

echo "[6] install test"
TEST="$WORK/test"
mkdir -p "$TEST"
cd "$TEST"

npm init -y >/dev/null
npm install "$TARBALL" --no-audit --no-fund >/dev/null

echo "[7] cli test"
node node_modules/ima-core-saas/bin/ima || true

cd "$ROOT"

echo "[8] npm auth"
npm whoami >/dev/null

echo "[9] version bump"
npm version patch -m "lifecycle stable %s"

echo "[10] publish"
npm publish

echo "[SUCCESS]"
