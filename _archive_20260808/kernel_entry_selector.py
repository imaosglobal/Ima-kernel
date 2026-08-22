from pathlib import Path
import json,time

BASE=Path(".")
RUNTIME=BASE/".ima/agi_evolution/runtime"

candidates=[]

files=RUNTIME/"canonical_kernel_candidates.txt"

for line in files.read_text().splitlines():
    p=Path(line.strip())

    if not p.exists():
        continue

    try:
        text=p.read_text(errors="ignore")
    except:
        continue

    score=0
    reasons=[]

    if "class Kernel" in text:
        score+=50
        reasons.append("Kernel class")

    if "def boot" in text:
        score+=20
        reasons.append("boot")

    if "def run" in text:
        score+=20
        reasons.append("run")

    if "ima.runtime" in text or ".ima/runtime" in str(p):
        score+=10
        reasons.append("runtime")

    if "backup" not in str(p).lower():
        score+=5
        reasons.append("non_backup")

    candidates.append({
        "file":str(p),
        "score":score,
        "reasons":reasons
    })


candidates.sort(
    key=lambda x:x["score"],
    reverse=True
)

result={
    "time":time.time(),
    "selected":candidates[:10]
}

(RUNTIME/"kernel_entry_selection.json").write_text(
    json.dumps(result,indent=2,ensure_ascii=False)
)

