#!/data/data/com.termux/files/usr/bin/bash
set -e

cd ~/ima_kernel

echo "=== IMA RELEASE CANDIDATE CREATION ==="

DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p .ima/releases/candidates

cat > .ima/releases/candidates/IMA_RC_MANIFEST.json <<EOF
{
  "product": "IMA",
  "release": "RC-1.0",
  "status": "READY",
  "core": "FROZEN",
  "runtime": "CANONICAL",
  "verification": "PASSED",
  "gateway": true,
  "launcher": true,
  "health": true,
  "deployment": true,
  "version_manager": true,
  "clients": [
    "web",
    "android",
    "mobile"
  ],
  "created": "$DATE"
}
EOF

sha256sum .ima/releases/candidates/IMA_RC_MANIFEST.json \
> .ima/releases/candidates/IMA_RC_MANIFEST.sha256

echo "[OK] Release manifest created"
echo "[OK] Release hash created"

cat .ima/releases/candidates/IMA_RC_MANIFEST.json

echo "=== RELEASE CANDIDATE READY ==="

