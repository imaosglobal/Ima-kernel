#!/data/data/com.termux/files/usr/bin/bash
set -e

echo "=== CREATE IMA CANONICAL WATCHDOG ==="

mkdir -p kernel/runtime/CANONICAL
mkdir -p .ima/governance


cat > kernel/runtime/CANONICAL/IMA_WATCHDOG.py <<'PY'
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

    if not HASH_FILE.exists():
        log("FAIL","missing_hash_manifest")
        return False

    ok=True

    for line in HASH_FILE.read_text().splitlines():

        if not line.strip():
            continue

        file,old=line.split(":",1)
        p=Path(file)

        if not p.exists():
            log("FAIL",{"missing":file})
            ok=False
            continue

        current=sha(p)

        if current != old:
            log("FAIL",{
                "modified":file,
                "expected":old,
                "actual":current
            })
            ok=False


    if ok:
        log("VERIFY_OK","canonical_state")

    return ok



def scan_duplicates():

    forbidden=[
        "IMA_SUPERVISOR.js",
        "SUPERVISOR.js",
        "daemon_supervisor",
        "master_supervisor",
        "runtime_duplicate"
    ]

    hits=[]

    for p in Path(".").rglob("*"):
        if any(x in str(p) for x in forbidden):
            hits.append(str(p))

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
PY


chmod +x kernel/runtime/CANONICAL/IMA_WATCHDOG.py


python3 kernel/runtime/CANONICAL/IMA_WATCHDOG.py


echo ""
echo "=== WATCHDOG CREATED ==="
echo "kernel/runtime/CANONICAL/IMA_WATCHDOG.py"

