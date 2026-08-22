from pathlib import Path
import json,time

BASE=Path(".")
RUNTIME=BASE/".ima/agi_evolution/runtime"

bad=[
"backup",
"archive",
"snapshot",
"server_",
"doctor",
"before_"
]

results=[]

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
        score+=100
        reasons.append("kernel.py")

    if "MOTHER_ENTRY" in p.name:
        score+=90
        reasons.append("mother_entry")

    if "class Kernel" in text:
        score+=80
        reasons.append("Kernel_class")

    if "ima.runtime" in text:
        score+=40
        reasons.append("runtime_import")

    if "def boot" in text:
        score+=20
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


results.sort(
    key=lambda x:x["score"],
    reverse=True
)

out={
"time":time.time(),
"count":len(results),
"top":results[:20]
}

(RUNTIME/"canonical_kernel_final_selection.json").write_text(
json.dumps(out,indent=2,ensure_ascii=False)
)


