from pathlib import Path
import json

root=Path(".")

targets=[
"api/server.py",
"conversation_layer.py",
"identity_context.py",
"ima_kernel.py",
"ima_system.py",
"ima_global.py",
"ima_brain.py",
"ima_chat.py",
"ima_mom.py"
]

report={}

for f in targets:
    p=root/f
    if p.exists():
        s=p.read_text(errors="ignore")
        report[f]={
            "exists":True,
            "imports":[x for x in [
                "conversation_layer",
                "identity_context",
                "memory",
                "kernel",
                "brain",
                "chat"
            ] if x in s],
            "size":p.stat().st_size
        }
    else:
        report[f]={"exists":False}

Path(".ima/reports/fusion_audit.json").write_text(
    json.dumps(report,ensure_ascii=False,indent=2),
    encoding="utf-8"
)

print(json.dumps(report,ensure_ascii=False,indent=2))
print("[OK] FUSION AUDIT COMPLETE")
