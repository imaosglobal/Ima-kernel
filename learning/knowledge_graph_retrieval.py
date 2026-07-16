
import json
from pathlib import Path

GRAPH = Path("learning/knowledge_graph.json")

ALIASES = {
    "מוזיקה": "music",
    "מוסיקה": "music",
    "מתמטיקה": "mathematics",
    "פסיכולוגיה": "psychology",
    "ביולוגיה": "biology",
    "פיזיקה": "physics",
    "בינה מלאכותית": "ai",
    "מדעי המחשב": "computer_science",
    "הנדסה": "engineering"
}


def load_graph():
    return json.loads(
        GRAPH.read_text(encoding="utf8")
    )["nodes"]


def extract_concepts(term):
    found = []

    low = term.lower()

    for heb, eng in ALIASES.items():
        if heb in term:
            found.append(eng)

    nodes = load_graph()

    for key, node in nodes.items():
        if key.lower() in low:
            found.append(key)

        if node.get("name", "").lower() in low:
            found.append(key)

    return list(set(found))


def search_concept(term):

    nodes = load_graph()
    concepts = extract_concepts(term)

    results = []

    for c in concepts:
        if c in nodes:

            results.append({
                "id": c,
                **nodes[c]
            })

            for r in nodes[c].get("relations", []):
                if r in nodes:
                    results.append({
                        "id": r,
                        **nodes[r],
                        "connection_from": c
                    })

    return results
