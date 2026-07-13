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


# --- IMA Pattern Memory Layer ---

import json
import time

PATTERN_MEMORY_FILE = "learning/learning_patterns.json"


def _load_patterns():
    try:
        with open(PATTERN_MEMORY_FILE,"r") as f:
            return json.load(f)
    except:
        return {"patterns":[]}


def _save_patterns(data):
    with open(PATTERN_MEMORY_FILE,"w") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )


def store_pattern(pattern):

    data=_load_patterns()

    for item in data["patterns"]:
        if item["pattern"] == pattern:
            item["count"] += 1
            item["last_seen"]=time.time()
            _save_patterns(data)
            return item

    item={
        "pattern":pattern,
        "count":1,
        "created":time.time(),
        "last_seen":time.time()
    }

    data["patterns"].append(item)

    _save_patterns(data)

    return item


def get_patterns(limit=10):

    data=_load_patterns()

    return sorted(
        data["patterns"],
        key=lambda x:x.get("count",0),
        reverse=True
    )[:limit]

