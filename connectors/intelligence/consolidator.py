import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

BASE = Path(__file__).parent.parent

MEMORY = BASE / "knowledge/software_memory.jsonl"
SUMMARY = BASE / "knowledge/concepts_memory.json"


def build():

    concepts = defaultdict(list)

    if MEMORY.exists():
        for line in MEMORY.read_text().splitlines():
            item=json.loads(line)

            concepts[item["concept"]].append(
                item
            )

    output={}

    for concept,items in concepts.items():

        confidence=max(
            x["confidence"]
            for x in items
        )

        output[concept]={
            "concept":concept,
            "confidence":confidence,
            "sources":[
                x["source"]
                for x in items
            ],
            "learned_from":len(items),
            "last_updated":datetime.now().isoformat()
        }


    SUMMARY.write_text(
        json.dumps(
            output,
            indent=2,
            ensure_ascii=False
        )
    )


if __name__=="__main__":
    build()
    print("CONCEPT MEMORY UPDATED")
