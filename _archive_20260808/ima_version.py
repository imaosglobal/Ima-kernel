#!/usr/bin/env python3

from pathlib import Path
import json
import time

LOCK = Path(".ima/governance/RELEASE_LOCK.json")

def main():


    if not LOCK.exists():
        return 1

    data=json.loads(LOCK.read_text())



    return 0


if __name__=="__main__":
    raise SystemExit(main())
