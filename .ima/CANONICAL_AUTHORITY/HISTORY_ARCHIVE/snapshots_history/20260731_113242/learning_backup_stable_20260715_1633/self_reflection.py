from pathlib import Path
import json
from datetime import datetime

JOURNAL = Path("learning/ima_journal.json")


def load_journal():
    try:
        return json.loads(
            JOURNAL.read_text(encoding="utf-8")
        )
    except Exception:
        return {
            "events": [],
            "improvements": [],
            "lessons": []
        }


def save_journal(data):
    JOURNAL.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )


def record_event(event, category="general"):
    journal = load_journal()

    journal["events"].append({
        "time": str(datetime.now()),
        "category": category,
        "event": event
    })

    save_journal(journal)


def add_lesson(lesson):
    journal = load_journal()

    journal["lessons"].append({
        "time": str(datetime.now()),
        "lesson": lesson
    })

    save_journal(journal)


def suggest_improvement(area, reason):
    journal = load_journal()

    journal["improvements"].append({
        "area": area,
        "reason": reason,
        "status": "pending"
    })

    save_journal(journal)


def reflection_report():
    journal = load_journal()

    return {
        "events": len(journal["events"]),
        "lessons": len(journal["lessons"]),
        "improvements": len(journal["improvements"]),
        "latest": journal["events"][-5:]
    }
