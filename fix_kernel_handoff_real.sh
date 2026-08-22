#!/data/data/com.termux/files/usr/bin/bash
set -e

BASE="$HOME/ima_kernel"
RUNTIME="$BASE/.ima/agi_evolution/runtime"

echo "[1] SEARCH REAL KERNEL"

python3 <<'PY'
from pathlib import Path
import json,time

BASE=Path(".")
RUNTIME=BASE/".ima/agi_evolution/runtime"

bad=[
"backup",
"archive",
"snapshot",
"stable_after",
"before_",
"broken"
]

found=[]

for p in BASE.rglob("*.py"):
    s=str(p).lower()

    if any(x in s for x in bad):
        continue

    try:
        text=p.read_text(errors="ignore")
    except:
        continue

    score=0
    reasons=[]

    if p.name=="kernel.py":
        score+=200
        reasons.append("kernel_file")

    if "class Kernel" in text:
        score+=150
        reasons.append("Kernel_class")

    if "MOTHER_ENTRY" in text:
        score+=120
        reasons.append("mother")

    if "ima.runtime" in text:
        score+=80
        reasons.append("runtime")

    if "def boot" in text:
        score+=20
        reasons.append("boot")

    if "def run" in text:
        score+=10
        reasons.append("run")

    if score:
        found.append({
            "file":str(p),
            "score":score,
            "reasons":reasons
        })

found.sort(key=lambda x:x["score"],reverse=True)

out={
"time":time.time(),
"count":len(found),
"selected":found[:20]
}

(RUNTIME/"real_kernel_selection.json").write_text(
json.dumps(out,indent=2,ensure_ascii=False)
)

PY


echo "[2] UPDATE HANDOFF"

python3 <<'PY'
from pathlib import Path
import json,time

R=Path(".ima/agi_evolution/runtime")

data=json.loads(
(R/"real_kernel_selection.json").read_text()
)

selected=data["selected"][0]

handoff={
"time":time.time(),
"status":"ready",
"selected_kernel":selected,
"next":"ima_master_runtime"
}

(R/"kernel_handoff_state.json").write_text(
json.dumps(handoff,indent=2,ensure_ascii=False)
)

PY


echo "[3] CONNECT MASTER RUNTIME"

python3 <<'PY'
from pathlib import Path
import json,time

p=Path(".ima/agi_evolution/runtime/ima_master_runtime.py")

text=p.read_text()

if "kernel_handoff_state.json" not in text:

    text=text.replace(
        'state={',
        '''handoff=load("kernel_handoff_state.json")

    state={'''
    )

    text=text.replace(
        '"decision":"continue"',
        '"decision":"continue",\n        "kernel":handoff'
    )

    p.write_text(text)

PY


echo "[4] TEST"

python3 -m py_compile \
.ima/agi_evolution/runtime/ima_master_runtime.py \
.ima/agi_evolution/runtime/brain_controller.py


python3 .ima/agi_evolution/runtime/ima_master_runtime.py


echo "[5] GIT"

git add .
git commit -m "IMA real kernel handoff to master runtime" || true
git push || true

echo "=== REAL KERNEL HANDOFF COMPLETE ==="

