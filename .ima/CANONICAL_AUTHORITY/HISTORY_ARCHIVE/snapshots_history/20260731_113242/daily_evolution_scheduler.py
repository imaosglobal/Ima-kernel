import json
from pathlib import Path
from datetime import datetime


BASE = Path.home()/".ima/evolution"
BASE.mkdir(parents=True, exist_ok=True)

PLAN = BASE/"daily_plan.json"
STATE = BASE/"scheduler_state.json"
NEXT = BASE/"next_session.json"


def load(path, default):
    if path.exists():
        try:
            return json.loads(path.read_text())
        except:
            return default
    return default


def save(path,data):
    path.write_text(
        json.dumps(
            data,
            indent=2,
            ensure_ascii=False
        )
    )


def schedule():

    plan = load(
        PLAN,
        {"goals":[]}
    )


    previous = load(
        STATE,
        {
            "completed":[],
            "history":[]
        }
    )


    goals = plan.get(
        "goals",
        []
    )


    # מנגנון חסכון:
    # לא יותר מ-3 משימות פעילות

    selected=[]

    for goal in goals:

        name=goal.get("goal")

        if name not in previous["completed"]:

            selected.append(
                {
                    "task":name,
                    "priority":goal.get(
                        "priority",
                        99
                    ),
                    "reason":goal.get(
                        "reason",
                        ""
                    )
                }
            )


        if len(selected)>=3:
            break


    result={

        "generated":
        datetime.now().isoformat(),

        "mode":
        "minimal_evolution",

        "next_tasks":
        selected,

        "rule":
        "learn_more_build_less"

    }


    save(
        NEXT,
        result
    )


    previous["history"].append(
        {
            "date":
            datetime.now().isoformat(),

            "selected":
            selected
        }
    )


    save(
        STATE,
        previous
    )


    print(
        "DAILY EVOLUTION SCHEDULED"
    )


if __name__=="__main__":
    schedule()
