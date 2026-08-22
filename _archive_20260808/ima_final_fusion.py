from pathlib import Path
import json
import time
import shutil
import hashlib

ROOT = Path(".")
IMA = ROOT / ".ima"
REPORT = IMA / "reports"

REPORT.mkdir(parents=True, exist_ok=True)

stamp = str(int(time.time()))
backup = ROOT / f"ima_backup_{stamp}"


backup.mkdir()
for name in [
    "api",
    "conversation_layer.py",
    "identity_context.py",
    "ima_chat.py",
    "IMA_IDENTITY.md",
    ".ima"
]:
    p = ROOT / name
    if p.exists():
        target = backup / name
        if p.is_dir():
            shutil.copytree(p, target)
        else:
            shutil.copy2(p, target)



files=[]

for p in ROOT.rglob("*"):
    if any(x in str(p) for x in [
        "node_modules",
        ".git",
        "__pycache__"
    ]):
        continue

    if p.is_file():
        files.append({
            "path":str(p),
            "size":p.stat().st_size,
            "type":p.suffix
        })

system_map={
    "timestamp":stamp,
    "files":files,
    "modules":[],
    "connections":[]
}

keywords=[
    "chat",
    "memory",
    "identity",
    "conversation",
    "kernel",
    "server",
    "runtime",
    "brain"
]

for f in files:
    low=f["path"].lower()
    for k in keywords:
        if k in low:
            system_map["modules"].append({
                "keyword":k,
                "file":f["path"]
            })


checks={
    "server":"api/server.py",
    "conversation":"conversation_layer.py",
    "identity":"identity_context.py",
    "legacy":".ima/legacy/ori_legacy.json"
}

for k,v in checks.items():
    system_map["connections"].append({
        "name":k,
        "exists":Path(v).exists(),
        "path":v
    })

out=REPORT/"system_map.json"

out.write_text(
    json.dumps(
        system_map,
        ensure_ascii=False,
        indent=2
    ),
    encoding="utf-8"
)


required=[
    ".ima/legacy/ori_legacy.json",
    "conversation_layer.py",
    "identity_context.py",
    "api/server.py"
]

ok=True

for r in required:
    if Path(r).exists():
    else:
        ok=False

lock={
    "system":"IMA",
    "state":"FUSION_READY" if ok else "INCOMPLETE",
    "timestamp":stamp,
    "next":"connect single runtime"
}

(IMA/"fusion_state.json").write_text(
    json.dumps(lock,ensure_ascii=False,indent=2),
    encoding="utf-8"
)


if ok:
else:

