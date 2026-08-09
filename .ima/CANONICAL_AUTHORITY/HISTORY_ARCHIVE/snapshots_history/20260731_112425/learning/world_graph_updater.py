
from learning.sources.html_extractor import extract_text
from pathlib import Path
import json

FILE=Path("learning/world_graph.json")
from learning.sources.html_extractor import extract_text
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
