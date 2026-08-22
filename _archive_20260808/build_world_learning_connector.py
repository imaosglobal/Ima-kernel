from pathlib import Path
import json
import time
import py_compile

base=Path("learning")
base.mkdir(exist_ok=True)

# External source layer
Path("learning/external_knowledge_source.py").write_text("""
def fetch_external(question):
    # placeholder connector
    # כאן יתחבר בעתיד API / ספריות / מסמכים
    knowledge={
        "מה זה חתול":{
            "content":"חתול הוא יונק ממשפחת החתוליים.",
            "domain":"biology"
        },
        "מה זה קוואנטום":{
            "content":"קוואנטום הוא תחום בפיזיקה המתאר מערכות ברמה האטומית והתת אטומית.",
            "domain":"physics"
        }
    }

    return knowledge.get(question)
""",encoding="utf8")


# Reliability layer
Path("learning/knowledge_validator.py").write_text("""
def validate(data):
    if not data:
        return False,0

    if "content" in data and len(data["content"])>10:
        return True,0.9

    return False,0.1
""",encoding="utf8")


# Store
Path("learning/world_knowledge_store.py").write_text("""
from pathlib import Path
import json

FILE=Path("learning/world_knowledge.json")

def save(question,data):
    if FILE.exists():
        store=json.loads(FILE.read_text(encoding="utf8"))
    else:
        store={}

    store[question]=data

    FILE.write_text(
        json.dumps(store,ensure_ascii=False,indent=2),
        encoding="utf8"
    )

    return store[question]
""",encoding="utf8")


# Graph update
Path("learning/world_graph_updater.py").write_text("""
from pathlib import Path
import json

FILE=Path("learning/world_graph.json")

def add_node(question,data):

    if FILE.exists():
        graph=json.loads(FILE.read_text(encoding="utf8"))
    else:
        graph={"nodes":[]}

    node={
        "id":question,
        "domain":data.get("domain"),
        "content":data.get("content"),
        "relations":[]
    }

    graph["nodes"].append(node)

    FILE.write_text(
        json.dumps(graph,ensure_ascii=False,indent=2),
        encoding="utf8"
    )

    return node
""",encoding="utf8")


# Memory
Path("learning/world_memory.py").write_text("""
from pathlib import Path
import json

FILE=Path("learning/world_memory.json")

def remember(question,data):

    if FILE.exists():
        mem=json.loads(FILE.read_text(encoding="utf8"))
    else:
        mem={}

    mem[question]=data

    FILE.write_text(
        json.dumps(mem,ensure_ascii=False,indent=2),
        encoding="utf8"
    )

    return True
""",encoding="utf8")


# Main connector
Path("learning/world_learning_connector.py").write_text("""
from learning.external_knowledge_source import fetch_external
from learning.knowledge_validator import validate
from learning.world_knowledge_store import save
from learning.world_graph_updater import add_node
from learning.world_memory import remember


def learn(question):

    source=fetch_external(question)

    if not source:
        return {
            "state":"NO_SOURCE",
            "question":question
        }


    ok,confidence=validate(source)

    if not ok:
        return {
            "state":"REJECTED"
        }


    stored=save(question,{
        **source,
        "confidence":confidence
    })


    node=add_node(question,stored)

    remember(question,stored)


    return {
        "state":"LEARNED",
        "store":stored,
        "node":node,
        "memory":True
    }
""",encoding="utf8")


for f in [
"learning/external_knowledge_source.py",
"learning/knowledge_validator.py",
"learning/world_knowledge_store.py",
"learning/world_graph_updater.py",
"learning/world_memory.py",
"learning/world_learning_connector.py"
]:
    py_compile.compile(f,doraise=True)


from learning.world_learning_connector import learn

tests=[
"מה זה חתול",
"מה זה קוואנטום",
"מה זה משהו שאין"
]

report={}

for t in tests:
    report[t]=learn(t)


Path(".ima/world_learning_connector_report.json").write_text(
json.dumps({
"time":time.time(),
"pipeline":
"External Source -> Validation -> Store -> Graph -> Memory",
"tests":report
},
ensure_ascii=False,
indent=2),
encoding="utf8"
)


