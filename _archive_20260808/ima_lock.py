#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import time

GOV = Path(".ima/governance")
GOV.mkdir(parents=True, exist_ok=True)

FILES = [
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

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():

    manifest={}

    for f in FILES:
        p=Path(f)
        if p.exists():
            manifest[f]=sha(p)

    release_hash=hashlib.sha256(
        json.dumps(manifest,sort_keys=True).encode()
    ).hexdigest()

    lock={
        "state":"CANONICAL_RELEASE_LOCKED",
        "release_hash":release_hash,
        "created":int(time.time()),
        "files":manifest,
        "policy":"single_canonical_runtime"
    }

    (GOV/"RELEASE_LOCK.json").write_text(
        json.dumps(lock,indent=2)
    )

    print("==============================")
    print(" IMA RELEASE LOCK")
    print("==============================")
    print("[OK] FILES REGISTERED")
    print("[OK] RELEASE HASH")
    print("[OK] CANONICAL LOCK ACTIVE")
    print("")
    print(release_hash)

if __name__=="__main__":
    main()
