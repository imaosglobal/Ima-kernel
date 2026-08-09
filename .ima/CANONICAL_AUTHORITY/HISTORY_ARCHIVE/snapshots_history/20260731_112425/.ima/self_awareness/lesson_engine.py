import json
from pathlib import Path
from datetime import datetime
from collections import Counter

EVENTS=Path(".ima/self_awareness/events.jsonl")
MEMORY=Path(".ima/self_awareness/long_term_memory.json")


def load_events():
    if not EVENTS.exists():
        return []

    return [
        json.loads(x)
        for x in EVENTS.read_text().splitlines()
    ]


def load_memory():
    if MEMORY.exists():
        return json.loads(MEMORY.read_text())

    return {
        "created":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "lessons":[]
    }


def learn():

    events=load_events()
    memory=load_memory()

    counter=Counter(
        e.get("event")
        for e in events
    )

    lessons=[]


    if counter.get("message_received",0)>0:
        lessons.append(
            "conversation_flow_exists"
        )

    if counter.get("health_check_completed",0)>0:
        lessons.append(
            "monitoring_system_active"
        )

    if counter.get("system_state_observed",0)>0:
        lessons.append(
            "system_stability_verified"
        )

    if counter.get("response_generated",0)>0:
        lessons.append(
            "response_pipeline_verified"
        )


    for lesson in lessons:
        if lesson not in [
            x["lesson"]
            for x in memory["lessons"]
        ]:
            memory["lessons"].append(
                {
                    "time":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "lesson":lesson
                }
            )


    MEMORY.write_text(
        json.dumps(
            memory,
            indent=2,
            ensure_ascii=False
        )
    )

    return memory


if __name__=="__main__":
    print(
        json.dumps(
            learn(),
            indent=2,
            ensure_ascii=False
        )
    )
