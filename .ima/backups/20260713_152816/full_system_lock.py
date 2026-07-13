import json, hashlib, time
from pathlib import Path

targets=[]

for folder in [
    "api",
    "android",
    "frontend",
    "ui",
    "agents",
    "learning",
    "kernel",
    ".ima/runtime"
]:
    p=Path(folder)
    if p.exists():
        for f in p.rglob("*"):
            if f.is_file():
                targets.append(str(f))

lock={
    "status":"FULL_SYSTEM_LOCKED",
    "timestamp":time.time(),
    "files":{},
    "count":len(targets)
}

for f in targets:
    try:
        lock["files"][f]=hashlib.sha256(
            Path(f).read_bytes()
        ).hexdigest()
    except:
        pass

Path(".ima/runtime/full_system_lock.json").write_text(
    json.dumps(lock,indent=2,ensure_ascii=False)
)

print("LOCKED FILES:",len(lock["files"]))
print("STATUS:",lock["status"])
