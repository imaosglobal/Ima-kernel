#!/data/data/com.termux/files/usr/bin/bash
set -e

R=".ima/agi_evolution/runtime"
REG="$R/CANONICAL_REGISTRY.json"

python3 - <<'PY'
import json, hashlib, pathlib, time

kernel="kernel/runtime/CANONICAL/python_bridge.py"
files=[
    kernel,
    ".ima/agi_evolution/runtime/ima_boot_gate.py",
    ".ima/agi_evolution/runtime/ima_master_runtime.py",
    "IMA_START_SINGLE_ENTRY.py"
]

registry={
    "time": time.time(),
    "mode":"canonical_only",
    "authority":"CANONICAL_REGISTRY",
    "entry_point":"IMA_START_SINGLE_ENTRY.py",
    "kernel":kernel,
    "handoff":"ima_master_runtime",
    "allowed_components":[],
    "blocked_fallback":True,
    "duplicate_registration":False
}

for f in files:
    p=pathlib.Path(f)
    if p.exists():
        registry["allowed_components"].append({
            "file":f,
            "sha256":hashlib.sha256(p.read_bytes()).hexdigest()
        })

pathlib.Path(".ima/agi_evolution/runtime/CANONICAL_REGISTRY.json").write_text(
    json.dumps(registry,indent=2),
    encoding="utf-8"
)

print(json.dumps(registry,indent=2))
PY

git add .ima/agi_evolution/runtime/CANONICAL_REGISTRY.json create_canonical_registry.sh
git commit -m "Create canonical component registry"
git push

echo "=== CANONICAL REGISTRY CREATED ==="
