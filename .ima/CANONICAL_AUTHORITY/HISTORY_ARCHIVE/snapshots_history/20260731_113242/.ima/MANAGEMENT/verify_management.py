from pathlib import Path
import json
import time

BASE = Path(".ima")
MANAGEMENT = BASE / "MANAGEMENT"

required = {
    "MANAGEMENT_STATE": MANAGEMENT / "MANAGEMENT_STATE.json",
    "ACTIVE_RUNTIME_INDEX": MANAGEMENT / "ACTIVE_RUNTIME_INDEX.json",
    "ACTIVE_CODE_INDEX": MANAGEMENT / "ACTIVE_CODE/ACTIVE_CODE_INDEX.json",
    "BACKUP_INDEX": MANAGEMENT / "BACKUP_INDEX.json",
    "BACKUP_STORE_INDEX": MANAGEMENT / "BACKUP_STORE/BACKUP_STORE_INDEX.json",
    "ARCHIVE_INDEX": MANAGEMENT / "ARCHIVE_INDEX.json",
    "ACTIVE_RUNTIME_MANIFEST": BASE / "ACTIVE_RUNTIME_MANIFEST.json",
    "CANONICAL_REGISTRY": BASE / "CANONICAL_AUTHORITY/governance/CANONICAL_REGISTRY.json"
}

print("=== MANAGEMENT LAYER VERIFICATION ===")

failed = []

for name, path in required.items():
    if path.exists():
        print("[OK]", name)
    else:
        print("[MISSING]", name)
        failed.append(name)

try:
    state = json.loads(
        required["MANAGEMENT_STATE"].read_text()
    )

    if (
        state.get("layer") == "MANAGEMENT_LAYER_ACTIVE"
        and state.get("status") == "CONNECTED"
    ):
        print("[OK] MANAGEMENT_STATE_VALID")
    else:
        print("[FAIL] MANAGEMENT_STATE_INVALID")
        failed.append("MANAGEMENT_STATE_INVALID")

except Exception:
    print("[FAIL] MANAGEMENT_STATE_READ_ERROR")
    failed.append("MANAGEMENT_STATE_READ_ERROR")


report = {
    "time": time.time(),
    "layer": "MANAGEMENT_LAYER",
    "status": "READY" if not failed else "FAILED",
    "failed": failed
}

out = MANAGEMENT / "latest_verification.json"
out.write_text(json.dumps(report, indent=2))

print()
print("STATUS:", report["status"])
print("REPORT:", out)
