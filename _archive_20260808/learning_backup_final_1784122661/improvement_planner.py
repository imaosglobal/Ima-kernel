from datetime import datetime


def classify_risk(item):

    high_risk = [
        "שינוי קוד",
        "מחיקה",
        "החלפת",
        "מבנה מערכת"
    ]

    for word in high_risk:
        if word in item:
            return "high"

    return "low"


def build_improvement_plan(suggestions):

    plan = []

    for suggestion in suggestions:

        risk = classify_risk(suggestion)

        priority = 1

        if "orchestrator" in suggestion.lower() or "learning" in suggestion:
            priority = 3

        elif "בדיקות" in suggestion or "מניעת" in suggestion:
            priority = 2

        plan.append({
            "time": str(datetime.now()),
            "suggestion": suggestion,
            "priority": priority,
            "risk": risk,
            "status": "planned"
        })

    return plan
