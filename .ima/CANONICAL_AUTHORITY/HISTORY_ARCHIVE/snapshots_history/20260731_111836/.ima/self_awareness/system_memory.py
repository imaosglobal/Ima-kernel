import json
from pathlib import Path
from datetime import datetime

STATE = Path(".ima/observer/system_state.json")
EVENTS = Path(".ima/self_awareness/events.jsonl")


def load_state():
    if not STATE.exists():
        return {}

    return json.loads(
        STATE.read_text()
    )


def load_events():
    if not EVENTS.exists():
        return []

    return [
        json.loads(x)
        for x in EVENTS.read_text().splitlines()
    ]


def summarize(limit=20):

    state = load_state()
    events = load_events()

    recent = events[-limit:]

    summary = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "health": state.get("health"),
        "components": len(
            state.get("components",[])
        ),
        "events_count": len(events),
        "recent_events": []
    }


    for e in recent:
        summary["recent_events"].append(
            {
                "time": e.get("time"),
                "event": e.get("event")
            }
        )


    return summary


def human_summary():

    s=summarize()

    text=[]

    text.append("=== IMA DAILY SUMMARY ===")
    text.append("")

    text.append(
        f"System Health: {s['health']}%"
    )

    text.append(
        f"Components: {s['components']}"
    )

    text.append(
        f"Events Recorded: {s['events_count']}"
    )

    text.append("")
    text.append("Recent events:")

    for e in s["recent_events"][-5:]:
        text.append(
            f"- {e['time']} {e['event']}"
        )

    return "\n".join(text)


if __name__=="__main__":
    print(human_summary())
