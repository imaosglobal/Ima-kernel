#!/data/data/com.termux/files/usr/bin/bash
set -e

BASE="$HOME/ima_kernel"
RUNTIME="$BASE/.ima/agi_evolution/runtime"

echo "[1] FIX CANONICAL FILTER"

cat > "$BASE/kernel_canonical_filter_final.py" <<'PY'
from pathlib import Path
import json,time

BASE=Path(".")
RUNTIME=BASE/".ima/agi_evolution/runtime"

IGNORE=[
"kernel_canonical_filter",
"kernel_entry_selector",
"verify_",
"build_",
"fix_",
"backup",
"archive",
"snapshot",
"server_",
"before_",
"runtime_snapshots"
]

results=[]

for p in BASE.rglob("*.py"):

    s=str(p).lower()

    if any(x in s for x in IGNORE):
        continue

    try:
        text=p.read_text(errors="ignore")
    except:
        continue

    score=0
    reasons=[]

    if p.name=="kernel.py":
        score+=200
        reasons.append("canonical_kernel")

    if "class Kernel" in text:
        score+=100
        reasons.append("Kernel_class")

    if "MOTHER_ENTRY" in p.name:
        score+=150
        reasons.append("mother_entry")

    if "ima.runtime" in text:
        score+=50
        reasons.append("runtime")

    if "def boot" in text:
        score+=30
        reasons.append("boot")

    if "def run" in text:
        score+=10
        reasons.append("run")

    if score:
        results.append({
            "file":str(p),
            "score":score,
            "reasons":reasons
        })

results.sort(key=lambda x:x["score"],reverse=True)

out={
"time":time.time(),
"count":len(results),
"top":results[:20]
}

(RUNTIME/"canonical_kernel_final_selection.json").write_text(
json.dumps(out,indent=2,ensure_ascii=False)
)

print(json.dumps(out,indent=2,ensure_ascii=False))
PY


echo "[2] RUN FILTER"

python3 kernel_canonical_filter_final.py


echo "[3] CREATE KERNEL HANDOFF"

python3 <<'PY'
from pathlib import Path
import json,time

root=Path(".ima/agi_evolution/runtime")

data=json.loads(
(root/"canonical_kernel_final_selection.json").read_text()
)

selected=data["top"][0] if data["top"] else {}

handoff={
"time":time.time(),
"status":"ready",
"selected_kernel":selected,
"next":"boot_gate"
}

(root/"kernel_handoff_state.json").write_text(
json.dumps(handoff,indent=2,ensure_ascii=False)
)

print(json.dumps(handoff,indent=2,ensure_ascii=False))
PY


echo "[4] PYTHON CHECK"

python3 -m py_compile \
kernel_canonical_filter_final.py \
.ima/agi_evolution/runtime/ima_boot_gate.py \
.ima/agi_evolution/runtime/ima_master_runtime.py


echo "[5] GIT"

git add .
git commit -m "IMA canonical kernel selector cleanup" || true
git push || true

echo "=== KERNEL SELECTOR FINAL READY ==="

