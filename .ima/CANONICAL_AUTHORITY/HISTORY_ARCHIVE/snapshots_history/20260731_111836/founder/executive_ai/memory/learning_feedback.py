import json
import time
from pathlib import Path

FILE=Path("founder/data/learning_feedback.json")


def save_feedback(question, action, result, lesson):

    data=[]

    if FILE.exists():
        data=json.loads(
            FILE.read_text()
        )

    data.append({
        "question": question,
        "action": action,
        "result": result,
        "lesson": lesson,
        "time": time.time()
    })

    FILE.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2
        )
    )

    return data[-1]


def get_feedback():

    if FILE.exists():
        return json.loads(
            FILE.read_text()
        )

    return []
