import json, hashlib
from pathlib import Path

LOCK=Path(".ima/runtime/system_integration_lock.json")

lock=json.loads(LOCK.read_text())

failed=[]
changed=[]

for file,old_hash in lock["components"].items():
    p=Path(file)
    if not p.exists():
        failed.append(file)
        continue

    new_hash=hashlib.sha256(p.read_bytes()).hexdigest()

    if new_hash != old_hash:
        changed.append({
            "file":file,
            "old":old_hash,
            "new":new_hash
        })

result={
    "status":"PASS" if not failed and not changed else "CHANGED",
    "missing":failed,
    "changed":changed
}

print(json.dumps(result,indent=2,ensure_ascii=False))
