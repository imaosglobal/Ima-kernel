#!/data/data/com.termux/files/usr/bin/bash
set -e

echo "=== IMA FINAL COMPLETION AUDIT ==="

python3 - <<'PY'
from pathlib import Path
import json
import time

ROOT = Path(".")

required = {
    "brain": "learning/meta_orchestrator.py",
    "orchestrator_connector": "learning/module_registry.py",
    "runtime": ".ima/runtime/runtime.py",
    "event_bus": "kernel/runtime/KERNEL_EVENT_BUS_V2.js",
    "api": "kernel/runtime/KERNEL_API_GATEWAY_V3.js",
    "persona": "learning/persona_engine.py",
    "learning": "learning/ima_learning_loop.py",
    "memory": ".ima/memory.json",
    "device": "kernel/device",
    "plugins": "kernel/plugins",
    "entry_gate": ".ima/governance/entry_gate_lock.json",
    "brain_lock": ".ima/governance/brain_registry.json",
    "architecture": ".ima/governance/canonical_architecture.json",
    "orchestrator_registry": ".ima/governance/orchestrator_registry.json"
}

report = {
    "system":"IMA",
    "time":time.time(),
    "components":{},
    "missing":[]
}

for name,path in required.items():
    ok = Path(path).exists()
    report["components"][name]={
        "path":path,
        "status":"OK" if ok else "MISSING"
    }
    if not ok:
        report["missing"].append(path)

Path(".ima/governance/final_completion_report.json").write_text(
    json.dumps(report,ensure_ascii=False,indent=2),
    encoding="utf-8"
)


if report["missing"]:
    for x in report["missing"]:
else:
PY

echo "=== RUNNING HEALTH ==="
python3 ima_full_system_check.py

echo "=== RUNNING ORCHESTRATOR ==="
python3 learning/module_registry.py

echo "=== COMPLETE ==="
