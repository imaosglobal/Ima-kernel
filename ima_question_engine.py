from pathlib import Path
import json
import sys
from datetime import datetime

HOME=Path.home()
TRUTH=HOME/".ima/truth/truth_database.jsonl"


from pathlib import Path

EVOLUTION=Path.home()/".ima/evolution"
KNOWLEDGE=Path.home()/".ima/memory/universal_knowledge_graph.json"


def load_json(path):
    try:
        import json
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def collect_ima_context():
    context=[]

    files=[
        EVOLUTION/"evolution_brain.json",
        EVOLUTION/"kernel_knowledge_bridge.json",
        EVOLUTION/"runtime_knowledge_state.json",
        EVOLUTION/"daily_plan.json",
        KNOWLEDGE
    ]

    for f in files:
        data=load_json(f)
        if data:
            context.append({
                "source":f.name,
                "data":data
            })

    return context

SYSTEM=HOME/".ima/evolution/system_truth.json"
EVOLUTION=HOME/".ima/evolution"


def load_json(path):
    try:
        return json.loads(path.read_text())
    except:
        return {}


def search_truth(words):
    results=[]

    if TRUTH.exists():
        for line in TRUTH.read_text().splitlines():
            try:
                item=json.loads(line)
                text=json.dumps(item,ensure_ascii=False)

                if any(w in text for w in words):
                    results.append(item)

            except:
                pass

    return results[-20:]


def answer(question):

    q=question.lower()

    words=q.split()

    today="2026-07-16"


    if any(x in q for x in ["היום","נוצר","עשינו","בוצע"]):



        for item in collect_ima_context():


        system=load_json(SYSTEM)

        if system:

        for file in EVOLUTION.glob("*.json"):

            data=load_json(file)

            if data:


        for e in search_truth(words+["2026-07-16","IMA"]):


    elif any(x in q for x in ["חסר","בעיה","לא עובד"]):

        data=load_json(SYSTEM)

        for x in data.get("missing_connections",[]):


    elif any(x in q for x in ["מצב","סטטוס","קור","מערכת"]):

        data=load_json(SYSTEM)

            data,
            indent=2,
            ensure_ascii=False
        ))


    else:

        results=search_truth(words)

        if results:
            for r in results:
                    r,
                    ensure_ascii=False
                )[:700])
        else:


if __name__=="__main__":
    answer(" ".join(sys.argv[1:]))
