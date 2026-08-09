from learning.learning_analyzer import analyze_learning
from learning.self_reflection import load_journal


def ima_awareness():

    analysis = analyze_learning()
    journal = load_journal()

    pending = [
        x for x in journal.get("improvements", [])
        if x.get("status") == "pending"
    ]

    return {
        "system_state": {
            "events": analysis["total_events"],
            "lessons": analysis["total_lessons"]
        },

        "observations": analysis["observations"],

        "pending_improvements": [
            x.get("reason")
            for x in pending
        ],

        "latest_lessons": journal.get("lessons", [])[-5:]
    }
