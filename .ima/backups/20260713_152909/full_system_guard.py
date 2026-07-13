import json, hashlib, time
from pathlib import Path

LOCK=Path(".ima/runtime/full_system_lock.json")

lock=json.loads(LOCK.read_text())

changed=[]
missing=[]

for f,old_hash in lock["files"].items():
    p=Path(f)

    if not p.exists():
        missing.append(f)
        continue

    new_hash=hashlib.sha256(
        p.read_bytes()
    ).hexdigest()

    if new_hash != old_hash:
        changed.append(f)

report={
    "status":"PASS" if not changed and not missing else "CHANGED",
    "timestamp":time.time(),
    "changed":changed,
    "missing":missing
}

Path(".ima/runtime/full_system_guard_report.json").write_text(
    json.dumps(report,indent=2,ensure_ascii=False)
)

print(json.dumps(report,indent=2,ensure_ascii=False))
