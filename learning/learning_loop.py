
from learning.learning_memory import store_pattern
import time


def learn_from_event(event):

    text = ""

    if isinstance(event, dict):
        data = event.get("data", {})

        if isinstance(data, dict):
            text = (
                str(data.get("text","")) +
                " " +
                str(data.get("question",""))
            )

    patterns=[]

    rules={
        "טכנולוגיה ומערכות":["מערכת","קוד","תכנות","AI","טכנולוגיה"],
        "פילוסופיה ותודעה":["תודעה","אמת","משמעות","נפש"],
        "יצירה והתפתחות":["יצירה","שיר","ללמוד","להתפתח"],
        "ריפוי והתבוננות":["כאב","ריפוי","רגש"]
    }

    for name,keys in rules.items():
        if any(k.lower() in text.lower() for k in keys):
            patterns.append(name)

    for p in patterns:
        store_pattern(p)

    return {
        "time":time.time(),
        "patterns":patterns,
        "status":"learned"
    }
