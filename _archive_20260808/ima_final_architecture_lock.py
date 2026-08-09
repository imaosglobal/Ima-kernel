from pathlib import Path
import json
import time
import hashlib

ROOT = Path(".")
GOV = ROOT / ".ima" / "governance"

GOV.mkdir(parents=True, exist_ok=True)

CANONICAL = {
    "brain": "learning/meta_orchestrator.py",
    "orchestrator": "learning/meta_orchestrator.py",
    "runtime": ".ima/runtime/runtime.py",
    "event_bus": "kernel/runtime/KERNEL_EVENT_BUS.js",
    "api_gateway": "kernel/runtime/KERNEL_API_GATEWAY.js",
    "persona": "learning/persona_engine.py",
    "learning": "learning/ima_learning_loop.py",
    "memory": ".ima/memory.json",
    "device": "kernel/device",
    "plugins": "kernel/plugins"
}

POLICY = {
    "system": "IMA",
    "state": "ARCHITECTURE_LOCKED",
    "created": time.time(),
    "rules": [
        "single_brain",
        "single_orchestrator",
        "single_runtime_registry",
        "no_duplicate_core_creation",
        "canonical_path_redirect",
        "verify_before_change"
    ],
    "canonical_components": CANONICAL
}

registry = GOV / "canonical_architecture.json"
registry.write_text(
    json.dumps(POLICY, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

checks = {}

for name,path in CANONICAL.items():
    p = ROOT / path
    checks[name] = {
        "path": path,
        "exists": p.exists(),
        "type": "directory" if p.is_dir() else "file"
    }

report = {
    "time": time.time(),
    "system": "IMA",
    "canonical_registry": str(registry),
    "components": checks
}

(GOV / "architecture_lock_report.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print("=== IMA ARCHITECTURE LOCK ===")
print("REGISTRY:", registry)

for k,v in checks.items():
    print(
        k,
        "OK" if v["exists"] else "MISSING",
        v["path"]
    )

print("ARCHITECTURE LOCK CREATED")
