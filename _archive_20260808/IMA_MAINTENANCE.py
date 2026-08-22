from pathlib import Path
import json
import time
import shutil

ROOT = Path(__file__).parent
BASE = ROOT / ".ima"
MANAGEMENT = BASE / "MANAGEMENT"
SNAPSHOTS = BASE / "snapshots"


required = [
    MANAGEMENT / "MANAGEMENT_STATE.json",
    MANAGEMENT / "latest_verification.json",
    BASE / "CANONICAL_AUTHORITY/governance/CANONICAL_REGISTRY.json",
    BASE / "ACTIVE_RUNTIME_MANIFEST.json"
]

failed = []

for p in required:
    if p.exists():
    else:
        failed.append(str(p))

if failed:
    status = "FAILED"
else:
    snapshot = SNAPSHOTS / f"maintenance_{int(time.time())}"
    snapshot.mkdir(parents=True, exist_ok=True)

    for src in [
        MANAGEMENT / "MANAGEMENT_STATE.json",
        MANAGEMENT / "latest_verification.json",
        MANAGEMENT / "status_report.json"
    ]:
        if src.exists():
            shutil.copy2(src, snapshot / src.name)


    status = "READY"

report = {
    "time": time.time(),
    "operation": "IMA_MAINTENANCE",
    "status": status,
    "failed": failed
}

out = MANAGEMENT / "maintenance_report.json"
out.write_text(json.dumps(report, indent=2))


if failed:
    raise SystemExit(1)
