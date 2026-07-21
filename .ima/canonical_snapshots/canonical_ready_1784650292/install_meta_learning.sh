#!/data/data/com.termux/files/usr/bin/bash

BASE=$HOME/ima_kernel
EV=$BASE/.ima/evolution

mkdir -p "$EV"


cat > "$BASE/evolution_brain.py" <<'PY'
import json
from pathlib import Path
from datetime import datetime

BASE=Path.home()/"ima_kernel"

CAP=BASE/".ima/evolution/system_capabilities.json"
HIST=BASE/".ima/evolution/git_history_memory.jsonl"
OUT=BASE/".ima/evolution/evolution_brain.json"


def load_json(p):
    if p.exists():
        try:
            return json.loads(p.read_text())
        except:
            return {}
    return {}


def analyze():

    capabilities=load_json(CAP)

    history=[]

    if HIST.exists():
        for line in HIST.read_text().splitlines():
            try:
                history.append(json.loads(line))
            except:
                pass


    brain={

        "generated":
        datetime.now().isoformat(),

        "system_understanding":{},

        "repeated_patterns":[],

        "missing_capabilities":[],

        "next_actions":[]

    }


    caps=capabilities.get(
        "capabilities",
        {}
    )


    brain["system_understanding"]=caps


    if "memory" in caps and "knowledge" in caps:
        brain["repeated_patterns"].append(
            "IMA has memory and knowledge layers"
        )


    if "kernel" in caps:
        brain["repeated_patterns"].append(
            "Kernel stabilization was a major evolution phase"
        )


    missing=[]


    existing=str(caps.keys())


    required=[
        "planning",
        "decision",
        "evaluation",
        "goal"
    ]


    for x in required:
        if x not in existing:
            missing.append(x)


    brain["missing_capabilities"]=missing


    brain["next_actions"]=[

        {
        "task":"connect knowledge router to kernel",
        "priority":1,
        "reason":"knowledge exists but runtime access is incomplete"
        },

        {
        "task":"build decision engine",
        "priority":2,
        "reason":"system needs selection ability"
        },

        {
        "task":"build autonomous planning",
        "priority":3,
        "reason":"convert understanding into action"
        }

    ]


    OUT.write_text(
        json.dumps(
            brain,
            indent=2,
            ensure_ascii=False
        )
    )


if __name__=="__main__":
    analyze()
    print("EVOLUTION BRAIN UPDATED")
PY



cat > "$BASE/goal_engine.py" <<'PY'
import json
from pathlib import Path


p=Path.home()/"ima_kernel/.ima/evolution/evolution_brain.json"

data=json.loads(p.read_text())


goals=[]


for x in data.get("missing_capabilities",[]):

    goals.append(
        {
        "goal":"create_"+x+"_engine",
        "importance":"high"
        }
    )


data["goals"]=goals


p.write_text(
    json.dumps(
        data,
        indent=2,
        ensure_ascii=False
    )
)


print("GOALS GENERATED")
PY



cat > "$BASE/decision_engine.py" <<'PY'
import json
from pathlib import Path


p=Path.home()/"ima_kernel/.ima/evolution/evolution_brain.json"

data=json.loads(p.read_text())


actions=data.get(
    "next_actions",
    []
)


for a in actions:

    if a["priority"]==1:
        a["decision"]="DO_FIRST"


data["decisions"]=actions


p.write_text(
    json.dumps(
        data,
        indent=2,
        ensure_ascii=False
    )
)


print("DECISIONS GENERATED")
PY



python "$BASE/evolution_brain.py"
python "$BASE/goal_engine.py"
python "$BASE/decision_engine.py"


echo "META LEARNING INSTALLED"

