#!/data/data/com.termux/files/usr/bin/bash

set -e

cd ~/ima_kernel

echo "=== IMA ONE COMMAND FUSION ==="

STAMP=$(date +%s)

echo "[1] BACKUP"
mkdir -p .ima/backups
cp -r .ima .ima/backups/ima_$STAMP 2>/dev/null || true

echo "[2] JSON VERIFY"
for f in .ima/legacy/ori_legacy.json .ima/fusion_lock.json; do
    if [ -f "$f" ]; then
        python3 -m json.tool "$f" >/dev/null
        echo "[OK] $f"
    else
        echo "[MISS] $f"
    fi
done

echo "[3] PYTHON VERIFY"

python3 -m py_compile \
ima_core_runtime.py \
ima_core_router.py \
identity_context.py \
conversation_layer.py \
api/server.py

echo "[OK] PYTHON"

echo "[4] CORE TEST"

python3 - <<'PY'
import ima_core_router as ima

tests=[
"מי אני?",
"מה החוקים שלי?",
"מה המטרה של IMA?"
]

for t in tests:
    r=ima.ask(t)
    print("\n---")
    print(t)
    print(r.get("response"))
    print("brain:",r.get("brain_connected"))
    print("mother:",r.get("mother_connected"))

print("\n[OK] CORE RESPONSE TEST")
PY


echo "[5] CREATE STATE"

cat > .ima/fusion_state.json <<JSON
{
 "system":"IMA",
 "state":"CORE_ROUTER_ACTIVE",
 "runtime":"ima_core_router.py",
 "identity":"identity_context.py",
 "memory":"conversation_layer.py",
 "brain":"ima_brain.py",
 "mother":"CONNECTED",
 "timestamp":"$STAMP"
}
JSON

chmod 600 .ima/fusion_state.json

echo "[6] START API"

pkill -f "python3 api/server.py" 2>/dev/null || true

nohup python3 api/server.py > ima_api.log 2>&1 &

sleep 2

echo "[7] API TEST"

curl -s \
-X POST http://127.0.0.1:8080/ask \
-H "Content-Type: application/json" \
-d '{"message":"מה המטרה של IMA?"}'


echo
echo "=== IMA FUSION COMPLETE ==="
