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

