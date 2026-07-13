import json
import hashlib
from pathlib import Path

GOV=Path(".ima/governance")
LOCK=GOV/"CANONICAL_ROOT_LOCK.json"
HASHES=GOV/"CANONICAL_HASHES.txt"

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def verify():

    if not LOCK.exists() or not HASHES.exists():
        return False

    lock=json.loads(LOCK.read_text())

    if lock.get("state")!="IMMUTABLE_CANONICAL":
        return False

    for line in HASHES.read_text().splitlines():
        if not line.strip():
            continue

        file,old=line.split(":",1)
        p=Path(file)

        if not p.exists():
            print("[FAIL] missing",file)
            return False

        if sha(p)!=old:
            print("[FAIL] hash",file)
            return False

    return True


if __name__=="__main__":
    if verify():
        print("[OK] CANONICAL ROOT VERIFIED")
        print("[OK] IMMUTABLE LOCK ACTIVE")
    else:
        print("[FAIL] CANONICAL ROOT")
        exit(1)
