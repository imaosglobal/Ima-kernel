import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / ".ima" / "global_index.json"
OUT = ROOT / ".ima" / "graph.json"

def relation(a, b):
    a_low = a.lower()
    b_low = b.lower()

    if "log" in a_low and "log" in b_low:
        return ("log_cluster", 0.9)

    if "core" in a_low and ".ima" in b_low:
        return ("system_dependency", 0.8)

    if "android" in a_low and "gradle" in b_low:
        return ("build_dependency", 0.7)

    return None

def main():
    with open(INDEX) as f:
        data = json.load(f)

    files = data.get("files", [])

    nodes = {}
    edges = []

    paths = [f["path"] for f in files]

    for f in files:
        nodes[f["path"]] = f

    for i in range(len(paths)):
        for j in range(i+1, len(paths)):
            a = paths[i]
            b = paths[j]

            r = relation(a, b)

            if r:
                etype, weight = r
                edges.append({
                    "from": a,
                    "to": b,
                    "type": etype,
                    "weight": weight
                })

    graph = {
        "nodes": nodes,
        "edges": edges
    }

    with open(OUT, "w") as f:
        json.dump(graph, f, indent=2)

    print("Nodes:", len(nodes))
    print("Edges:", len(edges))

if __name__ == "__main__":
    main()
