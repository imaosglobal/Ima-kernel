import json
from pathlib import Path

BASE = Path(__file__).parent.parent

knowledge = BASE / "knowledge/software_knowledge.jsonl"

def load_knowledge():
    items=[]
    if knowledge.exists():
        for line in knowledge.read_text().splitlines():
            try:
                items.append(json.loads(line))
            except:
                pass
    return items


def analyze():
    data=load_knowledge()

    domains={}
    skills=set()

    for item in data:
        domains.setdefault(item["domain"],[]).append(item["id"])
        for x in item.get("learns",[]):
            skills.add(x)

    return {
        "software_count":len(data),
        "domains":domains,
        "abilities":list(skills)
    }


if __name__=="__main__":
