from learning.self_reflection import load_journal, save_journal
from collections import Counter


def manage_learning():

    journal = load_journal()

    improvements = journal.get("improvements", [])
    lessons = journal.get("lessons", [])

    reasons = [
        x.get("reason")
        for x in improvements
        if x.get("reason")
    ]

    counts = Counter(reasons)

    cleaned = []
    seen = set()

    for item in improvements:
        reason = item.get("reason")

        if reason and reason not in seen:
            seen.add(reason)
            item["priority"] = counts[reason]
            cleaned.append(item)

    journal["improvements"] = cleaned

    save_journal(journal)

    return {
        "removed_duplicates": len(improvements) - len(cleaned),
        "remaining_improvements": len(cleaned),
        "lessons": len(lessons)
    }
