from pathlib import Path
import json, hashlib, sys

REG=Path(".ima/agi_evolution/runtime/CANONICAL_REGISTRY.json")

def verify():
    if not REG.exists():
        print("[BLOCK] CANONICAL REGISTRY MISSING")
        return False

    r=json.loads(REG.read_text())

    if r.get("mode")!="canonical_only":
        print("[BLOCK] INVALID MODE")
        return False

    for item in r.get("allowed_components",[]):
        p=Path(item["file"])

        if not p.exists():
            print("[BLOCK] MISSING:",p)
            return False

        h=hashlib.sha256(p.read_bytes()).hexdigest()

        if h != item["sha256"]:
            print("[BLOCK] HASH MISMATCH:",p)
            return False

    print("[OK] GLOBAL CANONICAL GUARD")
    return True

if __name__=="__main__":
    if not verify():
        sys.exit(1)
