#!/usr/bin/env python3

from pathlib import Path
import hashlib
import subprocess
import json
import time


ROOT=Path(".")
HASHFILE=ROOT/".ima/governance/CANONICAL_HASHES.txt"

CANONICAL=[
    "ima_master_runtime.py",
    "ima_core_runtime.py",
    "ima_fusion_runtime.py",
    "ima_integration_status.py",
    "IMA_START.py",
    "kernel/runtime/CANONICAL/python_bridge.py",
    "kernel/runtime/CANONICAL/IMA_SUPERVISOR.py",
    "kernel/runtime/CANONICAL/IMA_WATCHDOG.py"
]


REPORT=[]


def add(name, ok, detail=""):
    REPORT.append({
        "check":name,
        "status":"OK" if ok else "FAIL",
        "detail":detail
    })


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def check_files():
    missing=[]

    for f in CANONICAL:
        if not Path(f).exists():
            missing.append(f)

    add(
        "CANONICAL FILES",
        len(missing)==0,
        "missing="+str(missing)
    )


def check_hashes():

    if not HASHFILE.exists():
        add("HASH FILE",False,"missing")
        return

    failed=[]

    for line in HASHFILE.read_text().splitlines():
        if not line:
            continue

        f,h=line.split(":",1)
        p=Path(f)

        if not p.exists() or sha(p)!=h:
            failed.append(f)

    add(
        "HASH INTEGRITY",
        len(failed)==0,
        str(failed)
    )


def run_cmd(name,cmd):

    r=subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

    add(
        name,
        r.returncode==0,
        r.stdout.strip()[-300:]
    )


def main():

    print("================================")
    print("        IMA DOCTOR REPORT")
    print("================================")
    print("TIME:",int(time.time()))
    print("")

    check_files()
    check_hashes()

    run_cmd(
        "WATCHDOG",
        ["python3",
        "kernel/runtime/CANONICAL/IMA_WATCHDOG.py"]
    )

    run_cmd(
        "RUNTIME",
        ["python3",
        "-c",
        "import sys;sys.path.insert(0,'kernel/runtime/CANONICAL');import python_bridge;print(python_bridge.boot_runtime())"]
    )

    print("")

    for r in REPORT:
        print(
            "[{}] {} {}".format(
                r["status"],
                r["check"],
                r["detail"]
            )
        )

    print("")
    failed=[
        x for x in REPORT
        if x["status"]=="FAIL"
    ]

    if failed:
        print("=== RESULT: NEEDS REPAIR ===")
        return 1

    print("=== RESULT: IMA HEALTHY ===")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
