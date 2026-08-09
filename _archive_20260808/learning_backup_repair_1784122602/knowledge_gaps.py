from pathlib import Path
import json
from datetime import datetime

FILE = Path("learning/knowledge_gaps.json")


def load_gaps():
    try:
        return json.loads(
            FILE.read_text(encoding="utf-8")
        )
    except:
        return []


def save_gaps(data):
    FILE.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )


def record_gap(question):

    gaps = load_gaps()

    if question not in [x["question"] for x in gaps]:
        gaps.append({
            "time": str(datetime.now()),
            "question": question,
            "status": "pending"
        })

        save_gaps(gaps)


def get_gaps():
    return load_gaps()
