
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
