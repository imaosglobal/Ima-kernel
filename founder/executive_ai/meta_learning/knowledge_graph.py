from pathlib import Path
import json

FILE=Path("founder/data/knowledge_graph.json")


def store(node, relation=None):

    data=[]

    if FILE.exists():
        data=json.loads(FILE.read_text())

    item={
        "node":node,
        "relation":relation
    }

    data.append(item)

    FILE.parent.mkdir(parents=True,exist_ok=True)
    FILE.write_text(
        json.dumps(data,ensure_ascii=False,indent=2)
    )

    return item
