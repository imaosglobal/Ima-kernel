#!/usr/bin/env python3

import json
from pathlib import Path

ROOT = Path.home() / "ima_kernel"
ORCH = ROOT / ".ima" / "ORCHESTRATION"
RUNTIME = ORCH / "runtime"
EVIDENCE = RUNTIME / "automatic_cycles"

POLICY = {
    "schema": "ima.retention.policy.v1",
    "live_cycle_evidence": 100,
    "never_delete_provenance": True,
    "never_delete_generation_registry": True,
    "never_activate_historical_code": True,
}

(RUNTIME / "retention_policy.json").write_text(
    json.dumps(POLICY, indent=2),
    encoding="utf-8",
)

files = sorted(EVIDENCE.glob("cycle_*.json"))

keep = int(POLICY["live_cycle_evidence"])

if len(files) > keep:
    for p in files[:-keep]:
        archive = EVIDENCE / "archive"
        archive.mkdir(exist_ok=True)
        p.rename(archive / p.name)

print("[OK] retention policy applied")
print("[INFO] live automatic-cycle evidence:", min(len(files), keep))
