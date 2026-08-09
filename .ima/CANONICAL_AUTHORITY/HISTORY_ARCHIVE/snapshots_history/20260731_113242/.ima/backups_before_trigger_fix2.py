from pathlib import Path
import json
from datetime import datetime


EVENTS=Path(".ima/self_awareness/events.jsonl")
MARKER=Path(".ima/self_awareness/bridge/.last_report_event")


def should_report():

    if not EVENTS.exists():
        return False

    lines=EVENTS.read_text().splitlines()

    if not lines:
        return False

    last=json.loads(lines[-1])

    event_id=last.get("time","")+"_"+last.get("event","")

    if MARKER.exists():
        if MARKER.read_text()==event_id:
            return False

    MARKER.write_text(event_id)

    return last.get("event") in [
        "health_check_completed",
        "system_state_observed"
    ]


def trigger():

    return {
        "auto_report":should_report(),
        "time":datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


if __name__=="__main__":
    print(json.dumps(
        trigger(),
        indent=2,
        ensure_ascii=False
    ))
