import json
from pathlib import Path
from datetime import datetime

HOME=Path.home()

def load(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except:
        return {}


def get_today_events():
    import json
    from datetime import date

    events=[]
    truth=Path.home()/".ima/truth/truth_database.jsonl"

    if truth.exists():
        for line in truth.read_text(encoding="utf-8").splitlines():
            try:
                item=json.loads(line)
                if item.get("date")==str(date.today()):
                    events.append(item)
            except:
                pass

    return events


def summarize_today():
    result=[]

    for e in get_today_events():

        if e.get("source")=="git":
            result.append("Git: "+e.get("event",""))

        elif "evolution" in e.get("source",""):
            data=e.get("data",{})

            if "current_state" in data:
                for x in data["current_state"].get("engines_created_today",[]):
                    result.append("נוצר מנגנון: "+x)

        elif "current_state.json" in e.get("source",""):
            for x in e.get("data",{}).get("created_today",[]):
                result.append("נוצר היום: "+x)

    clean=[]
    seen=set()

    for item in result:
        key=item.lower().replace("_"," ").replace("מנגנון: ","")
        if key not in seen:
            seen.add(key)
            clean.append(item)

    final=[]
    normalized=set()

    for item in clean:
        key=item.lower()

        replacements={
            "נוצר מנגנון: ":"",
            "נוצר היום: ":"",
            "_":" "
        }

        for a,b in replacements.items():
            key=key.replace(a,b)

        key=" ".join(key.split())

        if key not in normalized:
            normalized.add(key)
            final.append(item)

    return final

def build_answer(question):

    truth=load(HOME/".ima/evolution/system_truth.json")
    brain=load(HOME/".ima/evolution/evolution_brain.json")
    plan=load(HOME/".ima/evolution/daily_plan.json")
    bridge=load(HOME/".ima/evolution/kernel_knowledge_bridge.json")

    print("IMA")
    print("================")
    print("שאלה:",question)
    print()

    if "היום" in question or "עשינו" in question:

        print("סיכום היום:")

        print("בוצעו היום:")

        actions=summarize_today()

        for a in actions:
            print("✅",a)

        print()
        print("רכיבים מאומתים:")

        for c in truth.get("verified_components",[]):
            print("  •",c["name"])

        print()

        if brain:
            for x in brain.get("current_state",{}).get("domains",[]):
                print("תחום:",x)

        print()

        missing=truth.get("missing_connections",[])
        if missing:
            print("עדיין חסר:")
            for m in missing:
                print("⚠️",m.replace("runtime consumption of knowledge","הליבה עדיין לא צורכת ידע בזמן ריצה").replace("automatic daily git checkpoint","עדיין אין שמירת Git יומית אוטומטית"))

    elif "חסר" in question:
        print("חוסרים ידועים:")
        for x in truth.get("missing_connections",[]):
            print("-",x)

    elif "הבא" in question or "המשך" in question:
        print("הצעדים הבאים:")
        for x in plan.get("goals",[]):
            print("-",x.get("goal"))

    else:
        print("נמצאו נתוני מערכת:")
        print(json.dumps(truth,ensure_ascii=False,indent=2))


if __name__=="__main__":
    import sys
    build_answer(" ".join(sys.argv[1:]))
