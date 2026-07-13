from learning.learning_analyzer import analyze_learning


def generate_improvements():

    report = analyze_learning()

    suggestions = []

    if report["total_events"] > 10:
        suggestions.append(
            "להרחיב ניתוח דפוסי שיחה לפי נושאים"
        )

    if report["pending_improvements"] > 0:
        suggestions.append(
            "לעבד הצעות שיפור קיימות ביומן"
        )

    observations = report.get("observations", [])

    if any("interaction" in x for x in observations):
        suggestions.append(
            "לשפר הבנת הקשר בין שיחות קודמות"
        )

    if not suggestions:
        suggestions.append(
            "להמשיך לאסוף ניסיון לפני שינוי מערכת"
        )

    return suggestions
