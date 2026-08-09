import json
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).parent.parent

GRAPH = BASE / "knowledge/universal_graph/knowledge_graph.json"


def load():
    if GRAPH.exists():
        return json.loads(GRAPH.read_text())
    return {
        "domains": {},
        "concepts": {},
        "relations": {},
        "patterns": {},
        "principles": {}
    }


def save(data):
    GRAPH.write_text(
        json.dumps(
            data,
            indent=2,
            ensure_ascii=False
        )
    )


def learn(domain, concept, source, confidence=0.5):

    data = load()

    data["domains"].setdefault(
        domain,
        []
    )

    if concept not in data["domains"][domain]:
        data["domains"][domain].append(concept)


    data["concepts"].setdefault(
        concept,
        {
            "sources":[],
            "confidence":0,
            "last_updated":None
        }
    )


    item=data["concepts"][concept]

    if source not in item["sources"]:
        item["sources"].append(source)

    item["confidence"]=max(
        item["confidence"],
        confidence
    )

    item["last_updated"]=datetime.now().isoformat()


    save(data)


def connect(a,b,relation):

    data=load()

    key=f"{a}->{b}"

    data["relations"][key]=relation

    save(data)


def add_pattern(name, concepts):

    data=load()

    data["patterns"][name]=concepts

    save(data)


if __name__=="__main__":

    learn(
        "software",
        "inventory",
        "erp",
        0.9
    )

    learn(
        "psychology",
        "identity",
        "therapy",
        0.8
    )

    learn(
        "music",
        "emotion",
        "composition",
        0.7
    )

    learn(
        "science",
        "pattern",
        "research",
        0.9
    )


    connect(
        "inventory",
        "business",
        "resource_management"
    )

    connect(
        "emotion",
        "music",
        "expression"
    )

    connect(
        "identity",
        "psychology",
        "self_understanding"
    )


    add_pattern(
        "human_system",
        [
            "identity",
            "emotion",
            "decision",
            "learning"
        ]
    )


    print("UNIVERSAL LEARNING ENGINE UPDATED")
