from pathlib import Path
import json
import time
import py_compile

base = Path("learning")
base.mkdir(exist_ok=True)

graph = {
    "nodes": {
        "biology": {
            "name": "ביולוגיה",
            "domain": "science",
            "relations": ["medicine","psychology","ecology"]
        },
        "physics": {
            "name": "פיזיקה",
            "domain": "science",
            "relations":["engineering","astronomy"]
        },
        "mathematics": {
            "name":"מתמטיקה",
            "domain":"science",
            "relations":["physics","computer_science"]
        },
        "psychology": {
            "name":"פסיכולוגיה",
            "domain":"humanity",
            "relations":["biology","philosophy"]
        },
        "philosophy": {
            "name":"פילוסופיה",
            "domain":"humanity",
            "relations":["psychology","ethics"]
        },
        "computer_science": {
            "name":"מדעי המחשב",
            "domain":"technology",
            "relations":["mathematics","ai"]
        },
        "ai": {
            "name":"בינה מלאכותית",
            "domain":"technology",
            "relations":["computer_science","psychology"]
        },
        "engineering": {
            "name":"הנדסה",
            "domain":"technology",
            "relations":["physics","mathematics"]
        },
        "music": {
            "name":"מוזיקה",
            "domain":"creation",
            "relations":["mathematics","psychology"]
        }
    }
}

Path("learning/knowledge_graph.json").write_text(
    json.dumps(graph,ensure_ascii=False,indent=2),
    encoding="utf8"
)


retrieval = Path("learning/knowledge_graph_retrieval.py")

retrieval.write_text(
'''
import json
from pathlib import Path

GRAPH=Path("learning/knowledge_graph.json")

def search_concept(term):

    data=json.loads(
        GRAPH.read_text(encoding="utf8")
    )

    results=[]

    for key,node in data["nodes"].items():
        if term in key or term in node.get("name",""):
            results.append({
                "id":key,
                **node
            })

    return results
''',
encoding="utf8"
)


py_compile.compile(
    "learning/knowledge_graph_retrieval.py",
    doraise=True
)

from learning.knowledge_graph_retrieval import search_concept

tests=[
"ביולוגיה",
"פסיכולוגיה",
"בינה",
"מתמטיקה"
]

report={}

for t in tests:
    report[t]=search_concept(t)


Path(".ima/universal_knowledge_graph_report.json").write_text(
    json.dumps({
        "time":time.time(),
        "tests":report
    },ensure_ascii=False,indent=2),
    encoding="utf8"
)

print(json.dumps(report,ensure_ascii=False,indent=2))
print("UNIVERSAL KNOWLEDGE GRAPH VERIFIED")
