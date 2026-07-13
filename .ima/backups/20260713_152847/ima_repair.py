#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import shutil
import time
import subprocess

ROOT = Path(".")
GOV = ROOT / ".ima" / "governance"
BACKUP = GOV / "repair_backup"

CANONICAL = [
    "kernel/runtime/CANONICAL/IMA_RUNTIME.js",
    "kernel/runtime/CANONICAL/IMA_STATE.js",
    "kernel/runtime/CANONICAL/IMA_EVENTS.js",
    "kernel/runtime/CANONICAL/IMA_HEAL.js",
    "kernel/runtime/CANONICAL/IMA_POLICY.js",
    "kernel/runtime/CANONICAL/python_bridge.py",
    "kernel/runtime/CANONICAL/IMA_SUPERVISOR.py",
    "kernel/runtime/CANONICAL/IMA_WATCHDOG.py",
    "IMA_START.py",
    "ima"
]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def log(msg):
    print(msg)

def rebuild_hashes():
    GOV.mkdir(parents=True, exist_ok=True)
    out=[]

    for f in CANONICAL:
        p=Path(f)
        if p.exists():
            out.append(f"{f}:{sha(p)}")

    (GOV/"CANONICAL_HASHES.txt").write_text(
        "\n".join(out)+"\n"
    )

    log("[OK] HASH MANIFEST REBUILT")

def backup():
    BACKUP.mkdir(parents=True, exist_ok=True)

    for f in CANONICAL:
        p=Path(f)
        if p.exists():
            target=BACKUP/f.replace("/","_")
            shutil.copy2(p,target)

    log("[OK] BACKUP CREATED")

def verify():
    r=subprocess.run(
        ["python3",
         "kernel/runtime/CANONICAL/IMA_WATCHDOG.py"],
        capture_output=True,
        text=True
    )

    print(r.stdout)

    return r.returncode==0

def main():

    print("==============================")
    print("       IMA SAFE REPAIR")
    print("==============================")
    print("TIME:",int(time.time()))
    print("")

    backup()
    rebuild_hashes()

    if verify():
        print("")
        print("=== REPAIR COMPLETE ===")
        print("[OK] IMA HEALTHY")
        return 0

    print("")
    print("=== REPAIR FAILED ===")
    return 1


if __name__=="__main__":
    raise SystemExit(main())
