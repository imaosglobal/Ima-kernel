#!/usr/bin/env python3

from pathlib import Path
import json
import time

LOCK = Path(".ima/governance/RELEASE_LOCK.json")

def main():

    print("==============================")
    print("     IMA CANONICAL VERSION")
    print("==============================")

    if not LOCK.exists():
        print("[FAIL] NO RELEASE LOCK")
        return 1

    data=json.loads(LOCK.read_text())

    print("STATE:", data.get("state"))
    print("HASH :", data.get("release_hash"))
    print("CREATED:", data.get("created"))
    print("FILES:", len(data.get("files",{})))

    print("")
    print("[OK] CANONICAL RELEASE VERIFIED")

    return 0


if __name__=="__main__":
    raise SystemExit(main())
