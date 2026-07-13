import os, json, hashlib
from pathlib import Path

ROOT=Path(".")
TARGETS=[
    "ima_master_runtime.py",
    "conversation_layer.py",
    "identity_context.py",
    ".ima/runtime/memory_bus.py",
    "learning/evolution_controller.py",
    "kernel/runtime/CANONICAL/python_bridge.py"
]

REPORT={
    "status":"AUDIT",
    "existing":[],
    "missing":[],
    "hashes":{}
}

for f in TARGETS:
    p=ROOT/f
    if p.exists():
        REPORT["existing"].append(str(f))
        h=hashlib.sha256(p.read_bytes()).hexdigest()
        REPORT["hashes"][str(f)]=h
    else:
        REPORT["missing"].append(str(f))

Path(".ima/runtime/integration_audit.json").write_text(
    json.dumps(REPORT,indent=2,ensure_ascii=False)
)

print(json.dumps(REPORT,indent=2,ensure_ascii=False))
