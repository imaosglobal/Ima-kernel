#!/data/data/com.termux/files/usr/bin/bash
set -e

BASE="$HOME/ima_kernel"
RUNTIME="$BASE/.ima/agi_evolution/runtime"

python3 <<'PY'
from pathlib import Path
import json,time

BASE=Path(".")
RUNTIME=BASE/".ima/agi_evolution/runtime"

exclude=[
"filter",
"selector",
"scan",
"check",
"build",
"fix_",
"verify",
"backup",
"archive",
"snapshot",
"before_",
"stable_after"
]

priority=[
"kernel.py",
"MOTHER_ENTRY.py"
]

results=[]

for p in BASE.rglob("*.py"):

    name=p.name

    if any(x in name.lower() for x in exclude):
        continue

    s=str(p)

    if any(x in s.lower() for x in [
        "/backups/",
        "/archive/",
        "/snapshots/"
    ]):
        continue

    try:
        text=p.read_text(errors="ignore")
    except:
        continue

    score=0
    reasons=[]

    if name=="kernel.py":
        score+=500
        reasons.append("canonical_kernel")

    if name=="MOTHER_ENTRY.py":
        score+=450
        reasons.append("mother_entry")

    if "kernel/runtime/CANONICAL" in s:
        score+=300
        reasons.append("canonical_runtime")

    if "class Kernel" in text:
        score+=200
        reasons.append("Kernel_class")

    if "def boot" in text:
        score+=50
        reasons.append("boot")

    if "def run" in text:
        score+=30
        reasons.append("run")

    if score:
        results.append({
            "file":str(p),
            "score":score,
            "reasons":reasons
        })


results.sort(
    key=lambda x:x["score"],
    reverse=True
)

out={
"time":time.time(),
"count":len(results),
"selected":results[:20]
}

(RUNTIME/"real_kernel_selection_v2.json").write_text(
json.dumps(out,indent=2,ensure_ascii=False)
)

print(json.dumps(out,indent=2,ensure_ascii=False))


if results:
    handoff={
    "time":time.time(),
    "status":"ready",
    "selected_kernel":results[0],
    "next":"ima_master_runtime"
    }

    (RUNTIME/"kernel_handoff_state.json").write_text(
        json.dumps(handoff,indent=2,ensure_ascii=False)
    )

    print("\nHANDOFF UPDATED")
    print(json.dumps(handoff,indent=2,ensure_ascii=False))

PY


python3 .ima/agi_evolution/runtime/ima_master_runtime.py


git add .
git commit -m "IMA real canonical kernel selector v2" || true
git push || true

echo "=== CANONICAL SELECTOR V2 READY ==="

