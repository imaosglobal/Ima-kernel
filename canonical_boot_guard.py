import json
import hashlib
import sys
from pathlib import Path

LOCK = Path(".ima/runtime/canonical_system_lock.json")

def verify():
    if not LOCK.exists():
        print("[FAIL] CANONICAL LOCK MISSING")
        return False

    lock=json.loads(LOCK.read_text())
    changed=[]
    missing=[]

    for f,h in lock.get("components",{}).items():
        p=Path(f)

        if not p.exists():
            missing.append(f)
            continue

        now=hashlib.sha256(p.read_bytes()).hexdigest()

        if now != h:
            changed.append(f)

    report={
        "status":"PASS" if not changed and not missing else "FAIL",
        "changed":changed,
        "missing":missing
    }

    Path(".ima/runtime/canonical_boot_guard.json").write_text(
        json.dumps(report,indent=2,ensure_ascii=False)
    )

    if report["status"]=="PASS":
        print("[OK] CANONICAL GUARD")
        return True

    print("[FAIL] CANONICAL GUARD")
    print(report)
    return False
