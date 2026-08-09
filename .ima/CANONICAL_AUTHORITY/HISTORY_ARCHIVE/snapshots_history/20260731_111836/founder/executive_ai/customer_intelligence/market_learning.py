import json
from pathlib import Path

FILE=Path("founder/data/customers/outreach_history.json")


def learn_patterns():

    if not FILE.exists():
        return {
            "total_interactions":0,
            "lessons":{}
        }

    data=json.loads(FILE.read_text())

    lessons={}

    for item in data:
        lesson=item.get("lesson","")

        if lesson:
            lessons[lesson]=lessons.get(
                lesson,
                0
            )+1

    return {
        "total_interactions":len(data),
        "lessons":lessons
    }
