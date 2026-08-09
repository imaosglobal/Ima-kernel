import json
from pathlib import Path
from datetime import datetime

EVENTS=Path(".ima/self_awareness/events.jsonl")
LESSONS=Path(".ima/self_awareness/long_term_memory.json")
KNOWLEDGE=Path(".ima/self_awareness/system_knowledge.json")


def load_json(path, default):
    if not path.exists():
        return default

    return json.loads(path.read_text())


def load_events():
    if not EVENTS.exists():
        return []

    return [
        json.loads(x)
        for x in EVENTS.read_text().splitlines()
    ]


def consolidate():

    events=load_events()

    lessons=load_json(
        LESSONS,
        {"lessons":[]}
    )

    knowledge={
        "updated":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "system":{
            "events_total":len(events),
            "health_observed":False,
            "stable":False
        },
        "conversation":{
            "active":False
        },
        "learning":{
            "lessons_count":len(
                lessons.get("lessons",[])
            )
        }
    }


    for e in events:

        if e.get("event")=="system_state_observed":
            knowledge["system"]["health_observed"]=True

            if e.get("data",{}).get("stable"):
                knowledge["system"]["stable"]=True


        if e.get("event")=="message_received":
            knowledge["conversation"]["active"]=True


    KNOWLEDGE.write_text(
        json.dumps(
            knowledge,
            indent=2,
            ensure_ascii=False
        )
    )

    return knowledge


if __name__=="__main__":
    print(
        json.dumps(
            consolidate(),
            indent=2,
            ensure_ascii=False
        )
    )
