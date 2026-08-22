#!/data/data/com.termux/files/usr/bin/bash
set -e

ROOT="$HOME/ima_kernel"
cd "$ROOT"

OUT=".ima/reports/product_layer_audit_$(date +%Y%m%d_%H%M%S).json"

echo "=== IMA PRODUCT LAYER AUDIT ==="

python3 - <<'PY'
from pathlib import Path
import json,time

root=Path(".")

core=[
"conversation_layer.py",
"IMA_START.py",
"kernel/runtime/CANONICAL/python_bridge.py",
"ima_master_runtime.py",
"identity_context.py"
]

product_targets={
"api":"api/server.py",
"web":"web",
"frontend":"frontend",
"android":"android",
"mobile":"mobile",
"ui":"ui",
"plugins":"plugins",
"modules":"modules",
"marketplace":"marketplace",
"auth":"auth",
"database":"database",
"docs":"docs",
"tests":"tests"
}

result={
"time":time.time(),
"core_protected":{},
"product_layer":{},
"python_modules":[],
"missing_product_components":[]
}

for f in core:
    p=Path(f)
    result["core_protected"][f]=p.exists()

for name,path in product_targets.items():
    p=Path(path)
    result["product_layer"][name]={
        "path":path,
        "exists":p.exists(),
        "type":"dir" if p.is_dir() else "file" if p.is_file() else "missing"
    }
    if not p.exists():
        result["missing_product_components"].append(name)

for p in Path(".").rglob("*.py"):
    if ".git" not in str(p) and ".ima" not in str(p):
        result["python_modules"].append(str(p))

out=Path(".ima/reports")
out.mkdir(parents=True,exist_ok=True)

file=out / f"product_layer_audit_{int(time.time())}.json"
file.write_text(
    json.dumps(result,indent=2,ensure_ascii=False),
    encoding="utf-8"
)

PY

echo "=== PRODUCT AUDIT COMPLETE ==="
