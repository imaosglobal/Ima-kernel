from learning.improvement_engine import generate_improvements
from learning.self_reflection import load_journal, save_journal
from datetime import datetime


def run_self_improvement():

    journal = load_journal()

    existing = [
        x.get("reason")
        for x in journal.get("improvements", [])
    ]

    new_items = []

    for item in generate_improvements():

        if item not in existing:

            journal["improvements"].append({
                "time": str(datetime.now()),
                "area": "self_learning",
                "reason": item,
                "status": "pending"
            })

            new_items.append(item)

    save_journal(journal)

    return new_items
