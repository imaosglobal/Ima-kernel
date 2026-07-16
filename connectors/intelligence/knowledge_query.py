import json
from pathlib import Path

BASE = Path(__file__).parent.parent

CONCEPTS = BASE / "knowledge/concepts_memory.json"


def get_concept(name):

    if not CONCEPTS.exists():
        return None

    data=json.loads(
        CONCEPTS.read_text()
    )

    return data.get(name)


def search(text):

    if not CONCEPTS.exists():
        return []

    data=json.loads(
        CONCEPTS.read_text()
    )

    results=[]

    for key,value in data.items():
        if text.lower() in key.lower():
            results.append(value)

    return results


if __name__=="__main__":

    import sys

    if len(sys.argv)>1:
        print(
            json.dumps(
                get_concept(sys.argv[1]),
                indent=2,
                ensure_ascii=False
            )
        )
