#!/usr/bin/env python3
from pathlib import Path
import subprocess
import time
import hashlib
import json

REPORT=[]

def add(name, ok, info=""):
    REPORT.append((name, ok, info))

def run(name, cmd):
    try:
        r=subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        add(name, r.returncode==0, r.stdout.strip()[-200:])
    except Exception as e:
        add(name, False, str(e))

def main():

    files=[
        "kernel/runtime/CANONICAL/IMA_RUNTIME.js",
        "kernel/runtime/CANONICAL/IMA_STATE.js",
        "kernel/runtime/CANONICAL/IMA_POLICY.js",
        "kernel/runtime/CANONICAL/IMA_SUPERVISOR.py",
        "kernel/runtime/CANONICAL/IMA_WATCHDOG.py",
        "IMA_START.py",
        "ima"
    ]

    missing=[f for f in files if not Path(f).exists()]
    add("CANONICAL FILES", len(missing)==0, str(missing))

    lock=Path(".ima/governance/RELEASE_LOCK.json")
    add("RELEASE LOCK", lock.exists(), str(lock))

    run(
        "WATCHDOG",
        ["python3","kernel/runtime/CANONICAL/IMA_WATCHDOG.py"]
    )

    run(
        "RUNTIME",
        [
            "python3",
            "-c",
        ]
    )

    mem=Path(".ima/memory.json")
    ledger=Path(".ima/ledger.jsonl")

    add("MEMORY", mem.exists(), str(mem))
    add("LEDGER", ledger.exists(), str(ledger))

    for name,ok,info in REPORT:
            "OK" if ok else "FAIL",
            name,
            info
        ))

    failed=[x for x in REPORT if not x[1]]

    if failed:
        return 1

    return 0

if __name__=="__main__":
    raise SystemExit(main())
