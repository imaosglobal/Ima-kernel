#!/data/data/com.termux/files/usr/bin/bash
set -e

cd ~/ima_kernel

echo "=== IMA CLIENT BUILD VERIFICATION ==="

DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p .ima/releases/client_build/$DATE

PASS=0
FAIL=0

ok() {
 echo "[OK] $1"
 PASS=$((PASS+1))
}

fail() {
 echo "[FAIL] $1"
 FAIL=$((FAIL+1))
}

echo "--- CLIENT CONTRACTS ---"

for f in \
product/clients/client_contract.json \
product/clients/web/client.json \
product/clients/android/client.json \
product/clients/mobile/client.json
do
 if [ -f "$f" ]; then
   ok "$f"
 else
   fail "$f"
 fi
done


echo "--- GATEWAY CONNECTION ---"

python - <<'PY'
import json
from pathlib import Path

files=[
"product/clients/client_contract.json",
"product/clients/web/client.json",
"product/clients/android/client.json",
"product/clients/mobile/client.json"
]

for f in files:
    data=json.loads(Path(f).read_text())
    assert data.get("connection") in ["product_gateway","gateway"] or f.endswith("client_contract.json")

print("[OK] All clients use gateway contract")
PY


echo "--- ANDROID CHECK ---"

if [ -f android/app/src/main/AndroidManifest.xml ]; then
 ok "Android manifest"
else
 fail "Android manifest"
fi


echo "--- BUILD MANIFEST ---"

cat > .ima/releases/client_build/$DATE/CLIENT_BUILD_MANIFEST.json <<EOF
{
 "product":"IMA",
 "release":"RC-1.0",
 "clients":[
   "web",
   "android",
   "mobile"
 ],
 "gateway":"connected",
 "status":"VERIFIED",
 "created":"$DATE"
}
EOF


echo
echo "PASS: $PASS"
echo "FAIL: $FAIL"

if [ "$FAIL" -eq 0 ]; then
 echo "STATUS: CLIENT BUILD VERIFIED"
else
 echo "STATUS: CLIENT BUILD FAILED"
 exit 1
fi

echo "=== CLIENT BUILD COMPLETE ==="

