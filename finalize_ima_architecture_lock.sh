#!/data/data/com.termux/files/usr/bin/bash
set -e

ROOT="$HOME/ima_kernel"

cd "$ROOT"

echo "=== IMA FINAL ARCHITECTURE LOCK ==="

mkdir -p .ima/governance

python3 - <<'PY'
from pathlib import Path
import json,time,hashlib

root=Path(".")

brain=Path("learning/meta_orchestrator.py")
runtime=Path("kernel/runtime/KERNEL_UNIFIED_RUNTIME_V1.js")

if not brain.exists():
    raise SystemExit("Missing canonical brain")

if not runtime.exists():
    raise SystemExit("Missing canonical runtime")


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


registry={
    "system":"IMA",
    "state":"LOCKED",
    "canonical_brain":str(brain),
    "canonical_runtime":str(runtime),
    "policy":[
        "single_brain_only",
        "single_runtime_only",
        "single_orchestrator_only",
        "block_duplicate_creation",
        "redirect_to_canonical_path",
        "require_snapshot_before_change",
        "require_health_check"
    ],
    "hashes":{
        str(brain):sha(brain),
        str(runtime):sha(runtime)
    },
    "locked_at":time.time()
}

Path(".ima/governance/architecture_lock.json").write_text(
    json.dumps(registry,indent=2,ensure_ascii=False),
    encoding="utf-8"
)

PY


chmod 444 .ima/governance/architecture_lock.json


cat > .ima/governance/DUPLICATE_CREATION_BLOCKED.json <<'EOF'
{
 "state":"LOCKED",
 "message":"IMA duplicate architecture creation blocked",
 "canonical_brain":"learning/meta_orchestrator.py",
 "canonical_runtime":"kernel/runtime/KERNEL_UNIFIED_RUNTIME_V1.js",
 "redirect":{
   "brain":"learning/meta_orchestrator.py",
   "runtime":"kernel/runtime/KERNEL_UNIFIED_RUNTIME_V1.js"
 }
}
EOF

chmod 444 .ima/governance/DUPLICATE_CREATION_BLOCKED.json


python3 ima_full_system_check.py

git add .ima/governance

git commit -m "IMA canonical architecture runtime brain lock" || true

git tag -a IMA_CANONICAL_ARCHITECTURE_LOCKED_v1 \
-m "IMA single canonical brain and runtime locked" || true

echo
echo "=== IMA LOCK COMPLETE ==="
echo "BRAIN: learning/meta_orchestrator.py"
echo "RUNTIME: kernel/runtime/KERNEL_UNIFIED_RUNTIME_V1.js"

