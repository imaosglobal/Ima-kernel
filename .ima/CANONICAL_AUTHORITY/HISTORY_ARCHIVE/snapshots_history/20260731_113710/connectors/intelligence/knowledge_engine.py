import json
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).parent.parent
MEMORY = BASE / "knowledge/software_memory.jsonl"
GRAPH = BASE / "knowledge/capability_graph.json"

def now():
    return datetime.now().isoformat()


def load():
    data={}
    if MEMORY.exists():
        for line in MEMORY.read_text().splitlines():
            try:
                item=json.loads(line)
                key=item["concept"]+"::"+item["source"]
                data[key]=item
            except:
                pass
    return data


def save(data):
    with open(MEMORY,"w",encoding="utf-8") as f:
        for item in data.values():
            f.write(json.dumps(item,ensure_ascii=False)+"\n")


def learn(concept,source,confidence=0.5):
    data=load()
    key=concept+"::"+source

    if key in data:
        data[key]["confidence"]=max(
            data[key]["confidence"],
            confidence
        )
        data[key]["last_updated"]=now()
    else:
        data[key]={
            "concept":concept,
            "source":source,
            "confidence":confidence,
            "first_seen":now(),
            "last_updated":now()
        }

    save(data)


def update_graph():
    data=load()

    graph={
        "nodes":{},
        "relations":{}
    }

    for item in data.values():
        graph["nodes"].setdefault(
            item["concept"],[]
        ).append(item["source"])

    for concept,sources in graph["nodes"].items():
        if len(sources)>1:
            graph["relations"][
                concept
            ]="shared_capability"

    GRAPH.write_text(
        json.dumps(
            graph,
            indent=2,
            ensure_ascii=False
        )
    )


if __name__=="__main__":
    learn("inventory","erp",0.9)
    learn("customers","crm",0.9)
    learn("payments","pos",0.8)
    update_graph()
    print("KNOWLEDGE UPDATED")
