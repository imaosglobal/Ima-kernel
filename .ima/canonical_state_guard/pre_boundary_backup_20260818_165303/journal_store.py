import json
import time
from pathlib import Path
from datetime import datetime

FILE = Path("founder/data/ima_learning_journal.json")


def add_entry(
    event_type,
    title,
    problem=None,
    solution=None,
    source="ima",
    category="general",
    importance=0,
    metadata=None
):

    entry = {
        "timestamp": time.time(),
        "datetime": datetime.now().isoformat(),
        "event_type": event_type,
        "title": title,
        "problem": problem,
        "solution": solution,
        "source": source,
        "category": category,
        "importance": importance,
        "metadata": metadata or {}
    }

    data = []

    if FILE.exists():
        data = json.loads(FILE.read_text(encoding="utf8"))

    data.append(entry)

    FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    FILE.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf8"
    )

    return entry


def get_all():

    if FILE.exists():
        return json.loads(
            FILE.read_text(encoding="utf8")
        )

    return []


def filter_by_category(category):

    return [
        x for x in get_all()
        if x.get("category") == category
    ]
