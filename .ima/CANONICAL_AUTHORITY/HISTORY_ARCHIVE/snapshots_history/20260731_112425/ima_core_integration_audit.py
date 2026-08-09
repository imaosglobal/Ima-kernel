from pathlib import Path
import json

modules=[
    "ima_core_runtime.py",
    "ima_brain.py",
    "ima_system.py",
    "ima_mom.py",
    "ima_global.py",
    "ima_chat.py",
    "ima_kernel.py",
    "conversation_layer.py",
    "identity_context.py"
]

report={}

for m in modules:
    p=Path(m)
    if not p.exists():
        report[m]={"status":"missing"}
        continue

    s=p.read_text(errors="ignore")

    report[m]={
        "status":"exists",
        "size":p.stat().st_size,
        "imports":[
            line.strip()
            for line in s.splitlines()
            if line.startswith("import ") or line.startswith("from ")
        ],
        "core_connection":{
            "uses_runtime":"ima_core_runtime" in s,
            "uses_identity":"identity_context" in s,
            "uses_memory":"memory" in s or "conversation" in s
        }
    }

Path(".ima/reports/core_integration_audit.json").write_text(
    json.dumps(report,ensure_ascii=False,indent=2),
    encoding="utf-8"
)

print(json.dumps(report,ensure_ascii=False,indent=2))
print("[OK] CORE INTEGRATION AUDIT COMPLETE")
