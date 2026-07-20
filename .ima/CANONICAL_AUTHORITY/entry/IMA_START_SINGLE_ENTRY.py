from pathlib import Path
import json,time,subprocess

R=Path(".ima/agi_evolution/runtime")

lock=json.loads((R/"CANONICAL_KERNEL_LOCK.json").read_text())

if not lock.get("locked"):
    raise SystemExit("KERNEL NOT LOCKED")


import hashlib

POLICY=R/"CANONICAL_RUNTIME_POLICY.json"

if not POLICY.exists():
    raise SystemExit("CANONICAL POLICY MISSING")

policy=json.loads(POLICY.read_text())

if policy.get("mode")!="canonical_only":
    raise SystemExit("NON CANONICAL MODE BLOCKED")

if policy.get("entry_point")!="IMA_START_SINGLE_ENTRY.py":
    raise SystemExit("WRONG ENTRY POINT")

kernel_path=Path(policy["kernel"])
if not kernel_path.exists():
    raise SystemExit("CANONICAL KERNEL MISSING")

expected=lock.get("sha256")

with open(kernel_path,"rb") as f:
    actual=hashlib.sha256(f.read()).hexdigest()

if expected and actual != expected:
    raise SystemExit(
        "CANONICAL HASH MISMATCH: "+actual
    )

if lock.get("fallback")!="disabled":
    raise SystemExit("FALLBACK ENABLED - BLOCKED")

print("[OK] CANONICAL POLICY VERIFIED")
print("[OK] HASH VERIFIED")
print("[OK] FALLBACK DISABLED")



# CANONICAL REGISTRY ENFORCEMENT
from pathlib import Path
import hashlib, json

REG=Path(".ima/agi_evolution/runtime/CANONICAL_REGISTRY.json")

if not REG.exists():
    raise SystemExit("CANONICAL REGISTRY MISSING")

registry=json.loads(REG.read_text())

if registry.get("mode") != "canonical_only":
    raise SystemExit("INVALID CANONICAL MODE")

for item in registry.get("allowed_components", []):
    f=Path(item["file"])
    if not f.exists():
        raise SystemExit(f"MISSING CANONICAL COMPONENT: {f}")

    h=hashlib.sha256(f.read_bytes()).hexdigest()
    if h != item["sha256"]:
        raise SystemExit(f"HASH MISMATCH: {f}")

print("[OK] CANONICAL REGISTRY VERIFIED")

print("=== IMA SINGLE ENTRY ===")
print("KERNEL:",lock["kernel"])
print("HANDOFF:",lock["handoff"])

boot=R/"ima_boot_gate.py"

subprocess.run(
    ["python3",str(boot)],
    check=True
)

master=R/"ima_master_runtime.py"

subprocess.run(
    ["python3",str(master)],
    check=True
)

import subprocess
subprocess.run(["python", ".ima/CANONICAL_AUTHORITY/entry/IMA_VALIDATE_ACTIVE.py"], check=True)
print("=== IMA SINGLE ENTRY COMPLETE ===")
