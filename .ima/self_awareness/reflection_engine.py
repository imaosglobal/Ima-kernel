import json
from pathlib import Path
from collections import Counter
from datetime import datetime

EVENTS = Path(".ima/self_awareness/events.jsonl")
STATE = Path(".ima/self_awareness/awareness_state.json")


def load_events():
    if not EVENTS.exists():
        return []

    return [
        json.loads(x)
        for x in EVENTS.read_text().splitlines()
    ]


def analyze():

    events = load_events()

    types = [
        e.get("event")
        for e in events
    ]

    counter = Counter(types)

    result = {
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_events": len(events),
        "event_frequency": dict(counter),
        "patterns": []
    }


    if counter.get("message_received",0) > 0:
        result["patterns"].append(
            "conversation_active"
        )

    if counter.get("health_check_completed",0) > 0:
        result["patterns"].append(
            "system_monitoring_active"
        )

    if counter.get("response_generated",0) > 0:
        result["patterns"].append(
            "response_pipeline_active"
        )


    STATE.write_text(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False
        )
    )

    return result


if __name__=="__main__":
    print(
        json.dumps(
            analyze(),
            indent=2,
            ensure_ascii=False
        )
    )
