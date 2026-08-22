#!/usr/bin/env python3
from pathlib import Path
import json,time

checks={
"canonical_runtime":Path("kernel/runtime/CANONICAL"),
"cli":Path("ima"),
"governance":Path(".ima/governance"),
"memory":Path(".ima/memory.json"),
"release_lock":Path(".ima/governance/RELEASE_LOCK.json"),
"api":Path("api"),
"frontend":Path("frontend"),
"android":Path("android")
}

report={}

for k,p in checks.items():
    report[k]={
        "exists":p.exists(),
        "path":str(p)
    }

Path(".ima/governance/PRODUCT_AUDIT.json").write_text(
json.dumps({
"time":int(time.time()),
"product_state":report
},indent=2)
)

for k,v in report.items():
        "[OK]" if v["exists"] else "[MISSING]",
        k,
        v["path"]
    )

