#!/data/data/com.termux/files/usr/bin/bash

ROOT="$HOME/ima_kernel/.ima/agi_evolution/runtime"

mkdir -p "$ROOT"

echo "[1] HEALTH MONITOR"

cat > "$ROOT/health_monitor.py" <<'PY'
from pathlib import Path
import json,time

ROOT=Path(".ima/agi_evolution/runtime")

def check():
    checks={}

    files=[
        "system_state.json",
        "module_registry.json",
        "latest_cycle.json"
    ]

    for f in files:
        checks[f]= (ROOT/f).exists()

    state={
        "time":time.time(),
        "healthy":all(checks.values()),
        "checks":checks
    }

    (ROOT/"health_state.json").write_text(
        json.dumps(state,indent=2)
    )

    return state


if __name__=="__main__":
    print(json.dumps(check(),indent=2))
PY


echo "[2] AUTO RESUME"

cat > "$ROOT/auto_resume.py" <<'PY'
from pathlib import Path
import json,time

ROOT=Path(".ima/agi_evolution/runtime")

STATE=ROOT/"resume_state.json"

def resume():

    data={
        "time":time.time(),
        "last_state":"detected",
        "next_action":"continue_evolution_cycle",
        "status":"ready"
    }

    STATE.write_text(
        json.dumps(data,indent=2)
    )

    return data


if __name__=="__main__":
    print(json.dumps(resume(),indent=2))
PY


echo "[3] SUPERVISOR"

cat > "$ROOT/ima_supervisor.py" <<'PY'
from pathlib import Path
import subprocess
import json,time,sys

ROOT=Path(".ima/agi_evolution/runtime")

def run():

    result={
        "time":time.time(),
        "steps":[]
    }

    jobs=[
        "health_monitor.py",
        "auto_resume.py"
    ]

    for job in jobs:
        try:
            out=subprocess.check_output(
                [sys.executable,str(ROOT/job)],
                text=True
            )

            result["steps"].append({
                "job":job,
                "status":"ok",
                "output":out[-300:]
            })

        except Exception as e:
            result["steps"].append({
                "job":job,
                "status":"failed",
                "error":str(e)
            })

    (ROOT/"supervisor_state.json").write_text(
        json.dumps(result,indent=2)
    )

    return result


if __name__=="__main__":
    print(json.dumps(run(),indent=2))
PY


echo "[4] TEST"

cd "$HOME/ima_kernel"

python3 .ima/agi_evolution/runtime/ima_supervisor.py


echo "[5] ADD CRON SUPERVISOR"

(crontab -l 2>/dev/null | grep -v "ima_supervisor.py"; \
echo "*/30 * * * * cd $HOME/ima_kernel && python3 .ima/agi_evolution/runtime/ima_supervisor.py >> $HOME/ima_kernel/.ima/agi_evolution/runtime/supervisor.log 2>&1") | crontab -


echo "=== SUPERVISOR LAYER READY ==="

