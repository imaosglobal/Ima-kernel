#!/data/data/com.termux/files/usr/bin/bash
set -e

R=".ima/agi_evolution/runtime"
LOCK="$R/CANONICAL_KERNEL_LOCK.json"
KERNEL="kernel/runtime/CANONICAL/python_bridge.py"

echo "=== HARDEN CANONICAL RUNTIME ==="

HASH=$(sha256sum "$KERNEL" | awk '{print $1}')

python3 - <<PY
import json

p="$LOCK"

with open(p) as f:
    x=json.load(f)

x["sha256"]="$HASH"
x["hash_algorithm"]="sha256"
x["enforcement"]="strict"
x["canonical_only"]=True
x["fallback"]="disabled"

with open(p,"w") as f:
    json.dump(x,f,indent=2)

print(json.dumps(x,indent=2))
PY

cat > "$R/CANONICAL_RUNTIME_POLICY.json" <<EOF
{
  "mode": "canonical_only",
  "entry_point": "IMA_START_SINGLE_ENTRY.py",
  "kernel": "kernel/runtime/CANONICAL/python_bridge.py",
  "handoff": "ima_master_runtime",
  "allow_direct_runtime_access": false,
  "allow_kernel_replacement": false,
  "hash_required": true
}
EOF

echo "=== POLICY CREATED ==="

git add "$LOCK" "$R/CANONICAL_RUNTIME_POLICY.json"

git commit -m "Harden canonical runtime with hash enforcement policy" || true

git push || true

echo "=== CANONICAL RUNTIME HARDENED ==="
