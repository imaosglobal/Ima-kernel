import json
from pathlib import Path
from datetime import datetime

BASE=Path.home()/"ima_kernel"

CAP=BASE/".ima/evolution/system_capabilities.json"
HIST=BASE/".ima/evolution/git_history_memory.jsonl"
OUT=BASE/".ima/evolution/evolution_brain.json"
OUT.parent.mkdir(parents=True, exist_ok=True)


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
