
import time
import json
from pathlib import Path


from learning.learning_memory import save_memory, load_memory


CONCLUSIONS_FILE = Path("learning/historical_conclusions.json")


def analyze_history(limit=500):

    from ima_brain import load_events

    events = load_events()[-limit:]

    counters = {
        "טכנולוגיה ומערכות": 0,
        "פילוסופיה ותודעה": 0,
        "יצירה והתפתחות": 0,
        "ריפוי והתבוננות": 0
    }

    for e in events:
        text = str(e).lower()

        if any(x in text for x in ["קוד","מערכת","ai","טכנולוגיה","תכנות"]):
            counters["טכנולוגיה ומערכות"] += 1

        if any(x in text for x in ["אמת","תודעה","משמעות","נפש","פילוסופיה"]):
            counters["פילוסופיה ותודעה"] += 1

        if any(x in text for x in ["שיר","יצירה","ללמוד","להתפתח"]):
            counters["יצירה והתפתחות"] += 1

        if any(x in text for x in ["כאב","ריפוי","רגש"]):
            counters["ריפוי והתבוננות"] += 1


    conclusions=[]

    if counters["טכנולוגיה ומערכות"]:
        conclusions.append(
            "נבנה דפוס חוזר של בניית מערכות, AI וזיכרון."
        )

    if counters["פילוסופיה ותודעה"]:
        conclusions.append(
            "קיים חיפוש עקבי אחר אמת, תודעה ומשמעות."
        )

    if counters["יצירה והתפתחות"]:
        conclusions.append(
            "יצירה ולמידה משמשות ככלים להבנה והתפתחות."
        )

    result={
        "time":time.time(),
        "events_analyzed":len(events),
        "patterns":counters,
        "conclusions":conclusions
    }

    CONCLUSIONS_FILE.write_text(
        json.dumps(result,ensure_ascii=False,indent=2)
    )

    return result


def get_conclusions():
    if CONCLUSIONS_FILE.exists():
        return json.loads(CONCLUSIONS_FILE.read_text())
    return analyze_history()
