#!/usr/bin/env python3

import json
import hashlib
import time
from pathlib import Path

ROOT=Path("kernel/runtime/CANONICAL")
GOV=Path(".ima/governance")

HASH_FILE=GOV/"CANONICAL_HASHES.txt"
LOG=GOV/"audit_log.jsonl"


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def log(event,data):
    with LOG.open("a") as f:
        f.write(json.dumps({
            "time":int(time.time()),
            "event":event,
            "data":data
        })+"\n")


def verify():

    mode_file = Path(".ima/governance/WATCHDOG_MODE.json")

    mode = "development"
    protected = []

    if mode_file.exists():
        data = json.loads(mode_file.read_text())
        mode = data.get("mode","development")
        protected = data.get("protected_layers",[])

    if not HASH_FILE.exists():
        log("INIT","creating_hash_manifest")
        return True

    updated=[]
    changed=[]

    for line in HASH_FILE.read_text().splitlines():

        if not line.strip():
            continue

        file,old=line.split(":",1)
        p=Path(file)

        if not p.exists():
            log("REMOVED",file)
            continue

        current=sha(p)

        if current != old:

            critical = any(
                file.startswith(x) or file == x
                for x in protected
            )

            changed.append(file)

            log("EVOLUTION_CHANGE",{
                "file":file,
                "old":old,
                "new":current,
                "critical":critical,
                "mode":mode
            })

            if critical and mode == "production":
                return False

        updated.append(f"{file}:{current}")

    HASH_FILE.write_text("\n".join(updated))

    if changed:
        log("HASH_AUTO_SYNC",changed)

    return True


def scan_duplicates():

    forbidden=[
        "IMA_SUPERVISOR.js",
        "SUPERVISOR.js",
        "daemon_supervisor",
        "master_supervisor"
    ]

    ignore=[
        ".git",
        ".ima/snapshots",
        "backup",
        "_quarantine",
        "graveyard",
        "IMA_WATCHDOG.py"
    ]

    hits=[]

    for p in Path(".").rglob("*"):

        sp=str(p)

        if any(x in sp for x in ignore):
            continue

        if not p.is_file():
            continue

        for bad in forbidden:
            if bad in p.name:
                hits.append(sp)

    if hits:
        log("DUPLICATE_DETECTED",hits)
        return False

    return True


def boot():

    a=verify()
    b=scan_duplicates()

    if a and b:
        return 0

    return 1



if __name__=="__main__":
    raise SystemExit(boot())
