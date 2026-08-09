from pathlib import Path
import json
import time

FILE = Path("founder/data/community_lessons.json")


def submit_lesson(lesson, source="community"):

    data = []

    if FILE.exists():
        data = json.loads(FILE.read_text(encoding="utf8"))

    item = {
        "timestamp": time.time(),
        "lesson": lesson,
        "source": source,
        "validated": False
    }

    data.append(item)

    FILE.parent.mkdir(parents=True, exist_ok=True)
    FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf8"
    )

    return item


def get_lessons():
    if FILE.exists():
        return json.loads(FILE.read_text(encoding="utf8"))

    return []
