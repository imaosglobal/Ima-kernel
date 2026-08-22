import json
from pathlib import Path

BASE = Path(__file__).parent.parent
GRAPH = BASE / "knowledge/graph/capability_graph.json"

def load_graph():
    if GRAPH.exists():
        return json.loads(GRAPH.read_text())
    return {}

def understand():
    graph = load_graph()

    return {
        "concepts": len(graph.get("nodes",{})),
        "relations": len(graph.get("relations",{})),
        "knowledge": graph
    }

if __name__ == "__main__":
        understand(),
        indent=2,
        ensure_ascii=False
    ))
