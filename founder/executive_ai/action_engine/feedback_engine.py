import json
from pathlib import Path
import time

FILE=Path("founder/data/action_feedback.json")


def save_feedback(target, action, response, lesson=""):

    data=[]

    if FILE.exists():
        data=json.loads(FILE.read_text())

    item={
        "target":target,
        "action":action,
        "response":response,
        "lesson":lesson,
        "time":time.time()
    }

    data.append(item)

    FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    FILE.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2
        )
    )

    return item


def get_feedback():

    if FILE.exists():
        return json.loads(
            FILE.read_text()
        )

    return []


def analyze_feedback():

    feedback=get_feedback()

    lessons=[]

    for item in feedback:

        if item.get("lesson"):
            lessons.append(
                item["lesson"]
            )

    return {
        "total_feedback":len(feedback),
        "lessons":lessons
    }
