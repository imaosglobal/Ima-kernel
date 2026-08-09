from learning.learning_scheduler import learning_cycle
from learning.self_reflection import load_journal, save_journal


THRESHOLD = 10


def check_learning_trigger():

    journal = load_journal()

    events = len(journal.get("events", []))

    if events > 0 and events % THRESHOLD == 0:
        result = learning_cycle()

        journal["events"].append({
            "category": "learning_cycle",
            "event": str(result)
        })

        save_journal(journal)

        return result

    return {
        "status": "waiting",
        "events": events,
        "next_cycle": THRESHOLD - (events % THRESHOLD)
    }
