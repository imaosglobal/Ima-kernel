import json
import os, json
from pathlib import Path

ROOT=Path(".")

targets={
    "API":"api",
    "Android":"android",
    "Frontend":"frontend",
    "UI":"ui",
    "Agents":"agents",
    "Learning":"learning",
    "Runtime":"kernel",
    "Memory":".ima/runtime"
}

report={
    "status":"SYSTEM_AUDIT",
    "connected":{},
    "missing":{},
    "memory_entry":".ima/runtime/memory_bus.py"
}

for name,path in targets.items():
    p=ROOT/path
    if p.exists():
        files=list(p.rglob("*"))
        py=[str(x) for x in files if x.suffix==".py"]

        report["connected"][name]={
            "path":str(path),
            "exists":True,
            "files":len(files),
            "python_files":len(py)
        }
    else:
        report["missing"][name]=str(path)

Path(".ima/runtime/system_connection_audit.json").write_text(
    json.dumps(report,indent=2,ensure_ascii=False)
)

print(json.dumps(report,indent=2,ensure_ascii=False))
