from pathlib import Path
import json

modules=[
"ima_core_router.py",
"ima_core_runtime.py",
"ima_system.py",
"ima_brain.py",
"ima_mom.py",
"ima_global.py",
"ima_chat.py",
"ima_kernel.py",
"conversation_layer.py",
"identity_context.py"
]

result={}

for m in modules:
    p=Path(m)
    if p.exists():
        text=p.read_text(errors="ignore")
        result[m]={
            "exists":True,
            "size":p.stat().st_size,
            "connections":{
                "identity":"identity_context" in text,
                "memory":"memory" in text or "conversation" in text,
                "brain":"brain" in text,
                "learning":"learning" in text,
                "mother":"mother" in text or "mom" in text,
                "router":"router" in text
            }
        }
    else:
        result[m]={"exists":False}

Path(".ima/reports/deep_integration.json").write_text(
json.dumps(result,ensure_ascii=False,indent=2),
encoding="utf-8"
)

print(json.dumps(result,ensure_ascii=False,indent=2))
print("[OK] DEEP INTEGRATION SCAN")
