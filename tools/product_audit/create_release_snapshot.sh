#!/data/data/com.termux/files/usr/bin/bash
set -e

cd ~/ima_kernel

echo "=== IMA RELEASE SNAPSHOT ==="

DATE=$(date +%Y%m%d_%H%M%S)
OUT=".ima/releases/snapshots/$DATE"

mkdir -p "$OUT"

echo "[1] Git state"
git rev-parse HEAD > "$OUT/COMMIT.txt"

echo "[2] Tags"
git tag -n > "$OUT/TAGS.txt"

echo "[3] Status"
git status --short > "$OUT/GIT_STATUS.txt"

echo "[4] Final manifest"
cp .ima/releases/final_release/IMA_FINAL_RELEASE.json "$OUT/"

echo "[5] Snapshot hash"
sha256sum \
"$OUT/IMA_FINAL_RELEASE.json" \
"$OUT/COMMIT.txt" \
"$OUT/TAGS.txt" \
> "$OUT/SNAPSHOT.sha256"

cat > "$OUT/SNAPSHOT_MANIFEST.json" <<EOF
{
 "product":"IMA",
 "release":"1.0",
 "status":"SNAPSHOT_SEALED",
 "commit":"$(git rev-parse HEAD)",
 "runtime":"CANONICAL",
 "core":"FROZEN",
 "created":"$DATE"
}
EOF

echo "[OK] Snapshot created"
echo "$OUT"
echo "=== SNAPSHOT COMPLETE ==="
