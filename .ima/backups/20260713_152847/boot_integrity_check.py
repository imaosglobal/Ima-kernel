import json
import subprocess
from pathlib import Path

checks={}

def run(cmd):
    try:
        r=subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True
        )
        return r.returncode==0
    except:
        return False

# full lock
checks["system_lock"]=Path(
    ".ima/runtime/full_system_lock.json"
).exists()

# memory fusion
try:
    x=json.load(open(".ima/runtime/memory_fusion_state.json"))
    checks["memory_fusion"]=x.get("status")=="ONLINE"
except:
    checks["memory_fusion"]=False

# integration lock
checks["integration_lock"]=Path(
    ".ima/runtime/system_integration_lock.json"
).exists()

# health endpoint
checks["api_health"]=run(
    "curl -s http://127.0.0.1:8080/health | grep -q ok"
)

report={
    "status":"ONLINE" if all(checks.values()) else "DEGRADED",
    "checks":checks
}

Path(".ima/runtime/boot_integrity_report.json").write_text(
    json.dumps(report,indent=2,ensure_ascii=False)
)

print(json.dumps(report,indent=2,ensure_ascii=False))
