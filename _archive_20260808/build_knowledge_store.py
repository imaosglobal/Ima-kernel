from pathlib import Path
import json
import time
import py_compile
import importlib

store = Path("learning/knowledge_store.json")
store.parent.mkdir(exist_ok=True)

knowledge = {
    "חתול": {
        "domain": "biology",
        "topic": "cat",
        "content": "חתול הוא יונק ממשפחת החתוליים. הוא בעל חיים מבוית שנפוץ כחיית מחמד. חתולים מתקשרים באמצעות קולות, שפת גוף וריח."
    },
    "תודעה": {
        "domain": "philosophy",
        "topic": "consciousness",
        "content": "תודעה היא היכולת לחוות חוויות, להיות מודע לעצמך ולסביבה, וליצור תפיסה פנימית של העולם."
    },
    "מתמטיקה": {
        "domain": "science",
        "topic": "mathematics",
        "content": "מתמטיקה היא תחום העוסק במספרים, מבנים, יחסים ודפוסים. היא משמשת במדע, הנדסה ומחשוב."
    },
    "מנוע בעירה": {
        "domain": "engineering",
        "topic": "combustion_engine",
        "content": "מנוע בעירה פנימית ממיר אנרגיה כימית לדחף מכני באמצעות שריפת דלק, יצירת לחץ והנעת בוכנות."
    }
}

store.write_text(
    json.dumps(
        knowledge,
        ensure_ascii=False,
        indent=2
    ),
    encoding="utf8"
)


retrieval = Path("learning/knowledge_retrieval.py")

retrieval.write_text(
'''
from pathlib import Path
import json

STORE = Path("learning/knowledge_store.json")

def retrieve(query):

    try:
        data=json.loads(
            STORE.read_text(encoding="utf8")
        )

        for key,value in data.items():
            if key in query:
                return value

    except Exception:
        return None

    return None
''',
encoding="utf8"
)


# verify
modules=[
"learning.knowledge_retrieval",
"learning.knowledge_answer_builder"
]

status={}

for m in modules:
    try:
        importlib.import_module(m)
        status[m]="OK"
    except Exception as e:
        status[m]="FAIL "+str(e)


py_compile.compile(
    "learning/knowledge_retrieval.py",
    doraise=True
)


from learning.knowledge_retrieval import retrieve

tests=[
"מה זה חתול",
"מהי תודעה",
"תסביר מתמטיקה",
"איך עובד מנוע בעירה"
]

results={}

for q in tests:
    results[q]=retrieve(q)


report={
"system":"IMA",
"component":"Knowledge Store + Retrieval",
"time":time.time(),
"modules":status,
"tests":results
}


Path(".ima/knowledge_store_report.json").write_text(
    json.dumps(report,ensure_ascii=False,indent=2),
    encoding="utf8"
)

