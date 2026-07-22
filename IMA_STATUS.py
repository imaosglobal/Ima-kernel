from pathlib import Path
import json
import hashlib
import time

ROOT = Path(__file__).parent
BASE = ROOT / ".ima"

print("=== IMA SYSTEM STATUS ===")

results = {}

# Management
management_state = BASE / "MANAGEMENT/MANAGEMENT_STATE.json"
if management_state.exists():
    state = json.loads(management_state.read_text())
    results["management"] = (
        state.get("status") == "CONNECTED"
        and state.get("layer") == "MANAGEMENT_LAYER_ACTIVE"
    )
else:
    results["management"] = False

# Canonical registry
registry = BASE / "CANONICAL_AUTHORITY/governance/CANONICAL_REGISTRY.json"
results["canonical_registry"] = registry.exists()

# Active manifest
manifest = BASE / "ACTIVE_RUNTIME_MANIFEST.json"
results["active_manifest"] = manifest.exists()

# Managed entry
results["managed_entry"] = (ROOT / "IMA_MANAGED_START.py").exists()

# Hash validation
hash_ok = True

if registry.exists():
    data = json.loads(registry.read_text())

    for item in data.get("allowed_components", []):
        path = ROOT / item["file"]

        if not path.exists():
            hash_ok = False
            break

        actual = hashlib.sha256(
            path.read_bytes()
        ).hexdigest()

        if actual != item["sha256"]:
            hash_ok = False
            break

results["canonical_hashes"] = hash_ok


failed = [
    k for k, v in results.items()
    if not v
]

report = {
    "time": time.time(),
    "status": "READY" if not failed else "FAILED",
    "checks": results,
    "failed": failed
}

out = BASE / "MANAGEMENT/status_report.json"
out.write_text(json.dumps(report, indent=2))

for k, v in results.items():
    print("[OK]" if v else "[FAIL]", k)

print()
print("STATUS:", report["status"])
print("REPORT:", out)
