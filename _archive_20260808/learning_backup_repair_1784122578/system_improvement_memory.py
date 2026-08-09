import json
from pathlib import Path

PATH = Path(".ima/system_improvements.json")


def load_system_improvements():

    if not PATH.exists():
        return {
            "status": "missing",
            "changes": {}
        }

    try:
        with open(PATH, encoding="utf-8") as f:
            return json.load(f)

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


def summarize_improvements():

    data = load_system_improvements()

    if "changes" not in data:
        return "אין רשומות שיפור מערכת."

    summary = []

    for component, changes in data["changes"].items():
        summary.append(
            component + ": " + ", ".join(changes)
        )

    return "\n".join(summary)
