from pathlib import Path
import json
from datetime import datetime

FILE = Path("learning/learning_memory.json")


def load_memory():
    try:
        return json.loads(FILE.read_text(encoding="utf-8"))
    except:
        return {
            "patterns": [],
            "successful_answers": [],
            "failed_answers": [],
            "decisions": []
        }


def save_memory(data):
    FILE.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )


def store_pattern(pattern):
    data = load_memory()

    data["patterns"].append({
        "time": str(datetime.now()),
        "pattern": pattern
    })

    save_memory(data)


def store_evaluation(question, score, note):
    data = load_memory()

    if score >= 0.8:
        data["successful_answers"].append({
            "question": question,
            "note": note
        })
    else:
        data["failed_answers"].append({
            "question": question,
            "note": note
        })

    save_memory(data)


def get_learning_memory():
    return load_memory()
