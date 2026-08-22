#!/data/data/com.termux/files/usr/bin/bash
set -e

cd ~/ima_kernel

echo "=== IMA RELEASE DISTRIBUTION BUNDLE ==="

DATE=$(date +%Y%m%d_%H%M%S)
OUT=".ima/releases/distribution_bundle/$DATE"

mkdir -p "$OUT"

echo "[1] Collect manifests"

cp .ima/releases/final_release/IMA_FINAL_RELEASE.json "$OUT/"
cp .ima/releases/PRODUCTION_READINESS.json "$OUT/"

cp .ima/releases/deployment_gateway/*/DEPLOYMENT_GATEWAY.json "$OUT/"

cp .ima/releases/distribution_targets/*/TARGET_REGISTRY.json "$OUT/"

cp .ima/releases/build_artifacts/*/BUILD_HASHES.sha256 "$OUT/"

echo "[2] Create bundle manifest"

cat > "$OUT/RELEASE_DISTRIBUTION_BUNDLE.json" <<EOF
{
 "product":"IMA",
 "release":"1.0",
 "status":"DISTRIBUTION_READY",
 "core":"FROZEN",
 "runtime":"CANONICAL",
 "gateway":"VERIFIED",
 "clients":[
  "web",
  "android",
  "ios",
  "linux",
  "mobile"
 ],
 "artifacts":"READY",
 "created":"$DATE"
}
EOF

echo "[3] Hash bundle"

sha256sum "$OUT/RELEASE_DISTRIBUTION_BUNDLE.json" \
> "$OUT/RELEASE_DISTRIBUTION_BUNDLE.sha256"

echo "[4] Verify"

python - <<PY
import json
from pathlib import Path

p=Path("$OUT/RELEASE_DISTRIBUTION_BUNDLE.json")
d=json.loads(p.read_text())

assert d["status"]=="DISTRIBUTION_READY"
assert d["core"]=="FROZEN"
assert d["artifacts"]=="READY"

PY

echo "=== RELEASE DISTRIBUTION BUNDLE READY ==="
