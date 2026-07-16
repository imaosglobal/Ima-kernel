from pathlib import Path
import json,time,subprocess

R=Path(".ima/agi_evolution/runtime")

lock=json.loads((R/"CANONICAL_KERNEL_LOCK.json").read_text())

if not lock.get("locked"):
    raise SystemExit("KERNEL NOT LOCKED")

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

print("=== IMA SINGLE ENTRY COMPLETE ===")
