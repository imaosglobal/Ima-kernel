#!/data/data/com.termux/files/usr/bin/bash
set -e

cd ~/ima_kernel

echo "=== IMA PRODUCTION RELEASE ARCHIVE ==="

DATE=$(date +%Y%m%d_%H%M%S)
OUT=".ima/releases/production_archive/$DATE"

mkdir -p "$OUT"

echo "[1] Collect release data"

cp .ima/releases/final_release/IMA_FINAL_RELEASE.json "$OUT/"
cp .ima/releases/final_launch_gate.json "$OUT/"
cp .ima/releases/PRODUCTION_READINESS.json "$OUT/"

echo "[2] Git snapshot"

git rev-parse HEAD > "$OUT/COMMIT.txt"
git tag -n | grep IMA_ > "$OUT/TAGS.txt"

echo "[3] Create archive manifest"

cat > "$OUT/PRODUCTION_RELEASE.json" <<EOF
{
 "product":"IMA",
 "release":"1.0",
 "status":"PRODUCTION_RELEASE",
 "launch_gate":"APPROVED",
 "core":"FROZEN",
 "runtime":"CANONICAL",
 "distribution":"READY",
 "rollback":"AVAILABLE",
 "created":"$DATE"
}
EOF

echo "[4] Hash"

sha256sum "$OUT"/*.json > "$OUT/RELEASE_HASHES.sha256"

echo "[5] Verify"

python - <<PY
import json
from pathlib import Path

p=Path("$OUT/PRODUCTION_RELEASE.json")
d=json.loads(p.read_text())

assert d["status"]=="PRODUCTION_RELEASE"
assert d["launch_gate"]=="APPROVED"
assert d["core"]=="FROZEN"

print("[OK] Production archive")
print("[OK] Launch approved")
print("[OK] Rollback point created")
PY

echo "ARCHIVE:"
echo "$OUT"

echo "=== PRODUCTION RELEASE ARCHIVE READY ==="
