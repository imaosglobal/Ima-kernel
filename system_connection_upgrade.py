import json
from pathlib import Path
import hashlib
import time

ROOT=Path(".")

targets={
    "UI":"ui",
    "Agents":"agents"
}

report={
    "status":"CONNECTION_UPGRADE",
    "created":time.time(),
    "connected":{},
    "created_paths":{}
}

for name,path in targets.items():
    p=ROOT/path

    if not p.exists():
        p.mkdir(parents=True)
        init=p/"__init__.py"
        init.write_text(
"""# IMA system connector
# connected to memory fusion layer
""",
encoding="utf-8"
        )

        report["created_paths"][name]=str(p)

    report["connected"][name]={
        "path":str(p),
        "exists":p.exists(),
        "memory_link":".ima/runtime/memory_bus.py"
    }


Path(".ima/runtime/system_connection_upgrade.json").write_text(
    json.dumps(report,indent=2,ensure_ascii=False)
)

print(json.dumps(report,indent=2,ensure_ascii=False))
