import json
from pathlib import Path

IMA_MEMORY = Path.home() / ".ima/memory"

SOFTWARE = IMA_MEMORY / "software_concepts.json"
UNIVERSAL = IMA_MEMORY / "universal_knowledge_graph.json"


def load_json(path):
    if path.exists():
        return json.loads(path.read_text())
    return {}


def search_software(term):
    data = load_json(SOFTWARE)

    results=[]

    for key,value in data.items():
        if term.lower() in key.lower():
            results.append({
                "type":"software",
                "data":value
            })

    return results


def search_universal(term):
    data = load_json(UNIVERSAL)

    results=[]

    concepts=data.get("concepts",{})

    for key,value in concepts.items():
        if term.lower() in key.lower():
            results.append({
                "type":"universal",
                "data":value
            })

    return results




def search_patterns(term):

    data = load_json(UNIVERSAL)

    results=[]

    patterns=data.get("patterns",{})

    for key,value in patterns.items():
        if term.lower() in key.lower():
            results.append({
                "type":"pattern",
                "data":value
            })

    return results


def ask(term):

    return {
        "query":term,
        "results":
            search_software(term)
            +
            search_universal(term)
            +
            search_patterns(term)
    }


if __name__=="__main__":

    import sys

    if len(sys.argv)>1:
        print(
            json.dumps(
                ask(sys.argv[1]),
                indent=2,
                ensure_ascii=False
            )
        )
