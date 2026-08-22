import json
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).parent.parent

GRAPH = BASE / "knowledge/universal_graph/knowledge_graph.json"
CONCEPTS = BASE / "knowledge/concepts_memory.json"


def load(path):
    if path.exists():
        return json.loads(path.read_text())
    return {}


def save(data):
    GRAPH.write_text(
        json.dumps(
            data,
            indent=2,
            ensure_ascii=False
        )
    )


def learn_patterns():

    graph = load(GRAPH)
    concepts = load(CONCEPTS)

    names=list(concepts.keys())

    graph.setdefault(
        "patterns",
        {}
    )

    if "business_system" not in graph["patterns"]:

        required=[
            "inventory",
            "customers",
            "orders",
            "payments"
        ]

        found=[
            x for x in required
            if x in names
        ]

        if len(found)>=3:

            graph["patterns"]["business_system"]={
                "detected":found,
                "confidence":0.8,
                "created":datetime.now().isoformat()
            }


    save(graph)


if __name__=="__main__":
    learn_patterns()
