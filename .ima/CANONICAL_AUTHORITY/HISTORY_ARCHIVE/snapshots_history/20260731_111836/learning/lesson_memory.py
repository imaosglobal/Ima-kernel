from pathlib import Path
from datetime import datetime
import json


LESSON_FILE = Path("learning/lessons.json")


def load_lessons():
    try:
        return json.loads(
            LESSON_FILE.read_text(encoding="utf-8")
        )
    except Exception:
        return {"lessons": []}


def save_lessons(data):
    LESSON_FILE.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def record_lesson(
    plan,
    evaluation,
    feedback,
):
    """
    Records a lesson from the evaluated planning pipeline.

    Append-only lesson memory.
    No execution.
    No self-modification.
    """

    data = load_lessons()

    lesson = {
        "timestamp": str(datetime.now()),
        "source": "autonomy_pipeline",
        "plan_status": plan.get("status"),
        "evaluation_status": evaluation.get("status"),
        "feedback_overall": feedback.get("overall"),
        "feedback": feedback.get("feedback", []),
        "execution": "disabled",
    }

    data.setdefault("lessons", []).append(lesson)
    save_lessons(data)

    return lesson


def get_lessons(limit=10):
    data = load_lessons()
    return data.get("lessons", [])[-limit:]
