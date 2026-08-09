import json
from datetime import datetime


ALLOWED_SYSTEM_FIELDS = [
    "stable",
    "events"
]

ALLOWED_LEARNING_FIELDS = [
    "lessons"
]

ALLOWED_REFLECTION = True


def filter_report(report):

    data = report.get("data", {})

    filtered = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": "safe_system_report",

        "system": {
            "stable":
                data.get("system",{}).get("stable"),

            "events":
                data.get("system",{}).get("events")
        },

        "learning": {
            "lessons":
                data.get("learning",{}).get("lessons")
        }
    }


    if ALLOWED_REFLECTION:
        filtered["reflection"] = data.get(
            "reflection",
            []
        )


    return filtered


if __name__=="__main__":
    from pathlib import Path

    p=Path(".ima/self_awareness/reports.jsonl")

    if p.exists():

        last=p.read_text().splitlines()[-1]

        report=json.loads(last)

        print(
            json.dumps(
                filter_report(report),
                indent=2,
                ensure_ascii=False
            )
        )
