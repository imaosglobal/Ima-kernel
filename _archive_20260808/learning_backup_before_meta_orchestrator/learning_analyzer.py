from learning.self_reflection import load_journal


def analyze_learning():

    journal = load_journal()

    events = journal.get("events", [])
    lessons = journal.get("lessons", [])
    improvements = journal.get("improvements", [])

    report = {
        "total_events": len(events),
        "total_lessons": len(lessons),
        "pending_improvements": len(improvements),
        "observations": []
    }

    categories = {}

    for event in events:
        cat = event.get("category", "unknown")
        categories[cat] = categories.get(cat, 0) + 1

    if categories:
        report["observations"].append(
            f"פעילות מרכזית: {categories}"
        )

    if len(events) > 10:
        report["observations"].append(
            "נאסף מספיק ניסיון כדי להתחיל לזהות דפוסים."
        )

    if len(improvements) > 0:
        report["observations"].append(
            "קיימות הצעות שיפור הממתינות לעיבוד."
        )

    return report
