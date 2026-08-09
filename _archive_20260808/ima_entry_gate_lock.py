from pathlib import Path
import json
import time

GOV = Path(".ima/governance")
GOV.mkdir(parents=True, exist_ok=True)

ENTRY = {
    "system": "IMA",
    "state": "ENTRY_GATE_LOCKED",
    "created": time.time(),

    "canonical_entry": {
        "brain": "learning/meta_orchestrator.py",
        "runtime": ".ima/runtime/runtime.py",
        "mission": ".ima/governance/mission_registry.json"
    },

    "rules": [
        "all_requests_through_entry_gate",
        "no_direct_core_access",
        "verify_before_execute",
        "single_execution_path"
    ]
}

path = GOV / "entry_gate_lock.json"

path.write_text(
    json.dumps(ENTRY, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print("=== IMA ENTRY GATE ===")
print("LOCKED:", path)
print("STATE: ENTRY_GATE_LOCKED")
