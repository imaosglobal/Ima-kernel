from pathlib import Path
import json
import time

base=Path("learning")
base.mkdir(exist_ok=True)

engine=base/"knowledge_expansion_engine.py"

engine.write_text("""
import json
from pathlib import Path
import time

STORE=Path("learning/knowledge_store.json")
GRAPH=Path("learning/knowledge_graph.json")

def load_store():
    if not STORE.exists():
        return {}
    return json.loads(STORE.read_text(encoding="utf8"))

def save_store(data):
    STORE.write_text(
        json.dumps(data,ensure_ascii=False,indent=2),
        encoding="utf8"
    )

def expand_knowledge(question, source="internal"):
    store=load_store()

    if question in store:
        return store[question]

    # מקום לחיבור API / מסמכים בעתיד
    result={
        "question":question,
        "content":"ידע חדש דורש מקור חיצוני מחובר",
        "source":source,
        "confidence":0.1,
        "time":time.time()
    }

    store[question]=result
    save_store(store)

    return result
""",encoding="utf8")


Path(".ima/knowledge_expansion_engine.lock").write_text(
json.dumps(
{
"state":"CREATED",
"pipeline":
"Unknown -> Expansion -> Store -> Graph -> Memory",
"time":time.time()
},
ensure_ascii=False,
indent=2
),
encoding="utf8"
)

print("KNOWLEDGE EXPANSION ENGINE CREATED")
