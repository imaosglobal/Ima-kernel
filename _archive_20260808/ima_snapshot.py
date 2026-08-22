#!/usr/bin/env python3
from pathlib import Path
import json
import hashlib
import time
import shutil

GOV = Path(".ima/governance")
SNAP = Path(".ima/snapshots")

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    SNAP.mkdir(parents=True, exist_ok=True)

    stamp = int(time.time())
    target = SNAP / f"canonical_snapshot_{stamp}"
    target.mkdir()

    files = [
        "IMA_START.py",
        "ima",
        "kernel/runtime/CANONICAL/IMA_RUNTIME.js",
        "kernel/runtime/CANONICAL/IMA_STATE.js",
        "kernel/runtime/CANONICAL/IMA_EVENTS.js",
        "kernel/runtime/CANONICAL/IMA_HEAL.js",
        "kernel/runtime/CANONICAL/IMA_POLICY.js",
        "kernel/runtime/CANONICAL/python_bridge.py",
        "kernel/runtime/CANONICAL/IMA_SUPERVISOR.py",
        "kernel/runtime/CANONICAL/IMA_WATCHDOG.py",
    ]

    manifest={}

    for f in files:
        p=Path(f)
        if p.exists():
            shutil.copy2(p, target / p.name)
            manifest[f]=sha(p)

    lock = {}
    release = GOV/"RELEASE_LOCK.json"
    if release.exists():
        lock=json.loads(release.read_text())

    snapshot={
        "state":"CANONICAL_SNAPSHOT",
        "created":stamp,
        "release_hash":lock.get("release_hash"),
        "files":manifest
    }

    (target/"SNAPSHOT.json").write_text(
        json.dumps(snapshot,indent=2)
    )


if __name__=="__main__":
    main()
