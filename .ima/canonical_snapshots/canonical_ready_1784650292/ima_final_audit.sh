#!/data/data/com.termux/files/usr/bin/bash

ROOT="$HOME/ima_kernel"
REPORT=".ima/governance/final_audit_report.json"
LOCK=".ima/governance/final_audit_lock.json"

echo "=== IMA FINAL AUDIT ==="

cd "$ROOT" || exit 1

mkdir -p .ima/governance

python3 - <<'PY'
from pathlib import Path
import json
import time

root = Path(".")
report = Path(".ima/governance/final_audit_report.json")

result = {
    "system": "IMA",
    "audit_time": time.time(),
    "checks": {}
}

checks = {
    "canonical_entry": Path("IMA_START.py").exists(),
    "brain_registry": Path(".ima/governance/brain_registry.json").exists(),
    "development_policy": Path(".ima/governance/development_policy.json").exists(),
    "orchestrator_registry": Path(".ima/governance/orchestrator_registry.json").exists(),
    "brain": Path("learning/meta_orchestrator.py").exists(),
    "connector": Path("learning/module_registry.py").exists()
}

for k,v in checks.items():
    result["checks"][k] = v

try:
    import subprocess
    r = subprocess.run(
        ["python3","IMA_START.py"],
        capture_output=True,
        text=True
    )
    result["ima_start_exit"] = r.returncode
    result["ima_start_output"] = r.stdout[-2000:]
    result["system_ready"] = r.returncode == 0
except Exception as e:
    result["system_ready"] = False
    result["error"] = str(e)

result["status"] = (
    "READY"
    if all(result["checks"].values()) and result.get("system_ready")
    else "FAILED"
)

report.write_text(
    json.dumps(result, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

lock = {
    "system": "IMA",
    "state": "AUDIT_LOCKED",
    "report": str(report),
    "locked_at": time.time(),
    "policy": [
        "no_new_brain",
        "no_new_orchestrator",
        "all_changes_through_IMA_START"
    ]
}

Path(".ima/governance/final_audit_lock.json").write_text(
    json.dumps(lock, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print("STATUS:", result["status"])
print("AUDIT SAVED:", report)
print("LOCK CREATED")
PY

chmod +x ima_final_audit.sh

echo "=== IMA FINAL AUDIT COMPLETE ==="
