import json
from pathlib import Path
from datetime import datetime

BASE=Path.home()/".ima/evolution"

brain_file=BASE/"evolution_brain.json"
goals_file=BASE/"goals.json"
decisions_file=BASE/"decisions.json"
plan_file=BASE/"daily_plan.json"


brain=json.loads(
    brain_file.read_text()
)


goals=[]

for item in brain.get("next_plan",[]):

    goals.append({
        "goal":item["task"],
        "priority":item["priority"],
        "reason":item["reason"],
        "created":datetime.now().isoformat()
    })


decisions=[]

for goal in goals:

    decisions.append({

        "action":goal["goal"],

        "decision":
        "SCHEDULE_NEXT",

        "priority":
        goal["priority"],

        "reason":
        goal["reason"]

    })


output={

    "generated":
    datetime.now().isoformat(),

    "goals":
    goals,

    "decisions":
    decisions,

    "rule":
    "minimum useful evolution"

}


goals_file.write_text(
    json.dumps(
        goals,
        indent=2,
        ensure_ascii=False
    )
)

decisions_file.write_text(
    json.dumps(
        decisions,
        indent=2,
        ensure_ascii=False
    )
)

plan_file.write_text(
    json.dumps(
        output,
        indent=2,
        ensure_ascii=False
    )
)


