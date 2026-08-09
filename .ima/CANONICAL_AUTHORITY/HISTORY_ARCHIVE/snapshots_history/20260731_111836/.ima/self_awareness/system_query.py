import json
from pathlib import Path

STATE = Path(".ima/observer/system_state.json")
EVENTS = Path(".ima/self_awareness/events.jsonl")


def get_system_state():
    if not STATE.exists():
        return {
            "health": "unknown",
            "components": []
        }

    return json.loads(
        STATE.read_text()
    )


def get_recent_events(limit=5):
    if not EVENTS.exists():
        return []

    lines = EVENTS.read_text().splitlines()

    return [
        json.loads(x)
        for x in lines[-limit:]
    ]


def format_status():

    state = get_system_state()

    text = []

    text.append("=== IMA SYSTEM STATUS ===")
    text.append("")

    for c in state.get("components", []):
        icon = "🟢" if c.get("status")=="OK" else "🔴"
        text.append(
            f"{c['name']} {icon} {c['status']}"
        )

    text.append("")
    text.append(
        f"Health: {state.get('health','unknown')}%"
    )

    events = get_recent_events(1)

    if events:
        text.append("")
        text.append(
            "Last event: " +
            events[0].get("event","")
        )

    return "\n".join(text)
