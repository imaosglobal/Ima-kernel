#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import time
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[3]
STATE=ROOT/".ima/governance/SUPERVISOR_STATE.json"

CANONICAL="kernel/runtime/CANONICAL/IMA_SUPERVISOR.py"


def digest():
    return hashlib.sha256(
        Path(__file__).read_bytes()
    ).hexdigest()


def verify():

    if not STATE.exists():
        return False

    data=json.loads(
        STATE.read_text()
    )

    return (
        data.get("canonical")==CANONICAL
        and data.get("hash")==digest()
    )


def boot():

    if not verify():
        print("[FAIL] SUPERVISOR INTEGRITY")
        return 1

    print("[OK] CANONICAL SUPERVISOR")
    print("[OK] HASH VERIFIED")
    print("[OK] LOCKED")

    return 0


if __name__=="__main__":
    sys.exit(boot())
