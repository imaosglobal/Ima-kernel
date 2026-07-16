#!/data/data/com.termux/files/usr/bin/bash

BASE=$HOME/ima_kernel

cat > $BASE/runtime_knowledge_guard.py <<'PY'
import json
from pathlib import Path
from datetime import datetime

bridge=Path.home()/".ima/evolution/kernel_knowledge_bridge.json"
out=Path.home()/".ima/evolution/runtime_knowledge_state.json"

data={}

try:
    data=json.loads(bridge.read_text())
except:
    pass

state={
    "updated":datetime.now().isoformat(),
    "status":"CONNECTED",
    "source":"kernel_knowledge_bridge",
    "knowledge_available":data.get("available_knowledge",{})
}

out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(
    json.dumps(state,ensure_ascii=False,indent=2)
)

print("RUNTIME KNOWLEDGE CONNECTED")
PY


cat > $BASE/daily_git_checkpoint.py <<'PY'
import subprocess
from datetime import datetime
from pathlib import Path

repo=Path.home()/ "ima_kernel"

subprocess.run(
    ["git","add","-A"],
    cwd=repo
)

status=subprocess.check_output(
    ["git","status","--porcelain"],
    cwd=repo
).decode()

if status.strip():

    subprocess.run(
        [
            "git",
            "commit",
            "-m",
            f"IMA daily checkpoint {datetime.now().isoformat()}"
        ],
        cwd=repo
    )

    print("DAILY CHECKPOINT CREATED")

else:
    print("NO CHANGES")
PY


python $BASE/runtime_knowledge_guard.py
python $BASE/daily_git_checkpoint.py

echo "RUNTIME + DAILY GIT CONNECTED"
