#!/data/data/com.termux/files/usr/bin/bash
set -e

echo "=== IMA CANONICAL ROOT LOCK ==="

ROOT="kernel/runtime/CANONICAL"
GOV=".ima/governance"

mkdir -p "$GOV"

FILES="
$ROOT/IMA_RUNTIME.js
$ROOT/IMA_STATE.js
$ROOT/IMA_EVENTS.js
$ROOT/IMA_HEAL.js
$ROOT/IMA_POLICY.js
$ROOT/python_bridge.py
$ROOT/IMA_SUPERVISOR.py
IMA_START.py
"

echo "=== VERIFY FILES ==="

HASH_DATA=""

for f in $FILES; do
    if [ ! -f "$f" ]; then
        echo "[FAIL] missing $f"
        exit 1
    fi

    H=$(sha256sum "$f" | awk '{print $1}')
    HASH_DATA="$HASH_DATA$f:$H\n"
    echo "[OK] $f"
done


printf "$HASH_DATA" > "$GOV/CANONICAL_HASHES.txt"


ROOT_HASH=$(sha256sum "$GOV/CANONICAL_HASHES.txt" | awk '{print $1}')


cat > "$GOV/CANONICAL_ROOT_LOCK.json" <<EOF
{
 "state":"IMMUTABLE_CANONICAL",
 "root":"kernel/runtime/CANONICAL",
 "root_hash":"$ROOT_HASH",
 "policy":"one_runtime_one_supervisor_one_entry",
 "verify_on_boot":true,
 "forbidden_duplicates":[
   "IMA_SUPERVISOR.js",
   "SUPERVISOR.js",
   "daemon_supervisor",
   "master_supervisor",
   "runtime_backup",
   "runtime_duplicate"
 ]
}
EOF


cat > verify_canonical_root.py <<'PY'
import json
import hashlib
from pathlib import Path

GOV=Path(".ima/governance")
LOCK=GOV/"CANONICAL_ROOT_LOCK.json"
HASHES=GOV/"CANONICAL_HASHES.txt"

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def verify():

    if not LOCK.exists() or not HASHES.exists():
        return False

    lock=json.loads(LOCK.read_text())

    if lock.get("state")!="IMMUTABLE_CANONICAL":
        return False

    for line in HASHES.read_text().splitlines():
        if not line.strip():
            continue

        file,old=line.split(":",1)
        p=Path(file)

        if not p.exists():
            print("[FAIL] missing",file)
            return False

        if sha(p)!=old:
            print("[FAIL] hash",file)
            return False

    return True


if __name__=="__main__":
    if verify():
        print("[OK] CANONICAL ROOT VERIFIED")
        print("[OK] IMMUTABLE LOCK ACTIVE")
    else:
        print("[FAIL] CANONICAL ROOT")
        exit(1)
PY


chmod +x verify_canonical_root.py


echo ""
echo "=== VERIFY ROOT ==="
python3 verify_canonical_root.py

echo ""
echo "=== CANONICAL ROOT LOCKED ==="
echo "$ROOT"
