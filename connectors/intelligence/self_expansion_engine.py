import json
from pathlib import Path
from datetime import datetime


BASE=Path(__file__).parent.parent

CONCEPTS=BASE/"knowledge/concepts_memory.json"
SOFTWARE=Path.home()/".ima/memory/software_concepts.json"
GRAPH=BASE/"knowledge/universal_graph/knowledge_graph.json"


def load(path):
    if path.exists():
        return json.loads(path.read_text())
    return {}


def save(data):
    GRAPH.write_text(
        json.dumps(
            data,
            indent=2,
            ensure_ascii=False
        )
    )


def expand():

    graph=load(GRAPH)

    concepts=set()

    for source in [
        CONCEPTS,
        SOFTWARE
    ]:

        data=load(source)

        if isinstance(data,dict):
            concepts.update(
                data.keys()
            )


    domains=graph.setdefault(
        "domains",
        {}
    )


    rules={

        "business":[
            "inventory",
            "customers",
            "orders",
            "payments"
        ],

        "ai":[
            "automation",
            "learning",
            "decision"
        ],

        "human_system":[
            "identity",
            "emotion",
            "decision",
            "learning"
        ]

    }


    for domain,signals in rules.items():

        found=[
            x for x in signals
            if x in concepts
        ]


        if len(found)>=2:

            domains[domain]={
                "detected_from":found,
                "confidence":
                round(
                    len(found)/len(signals),
                    2
                ),
                "updated":
                datetime.now().isoformat()
            }


    save(graph)


if __name__=="__main__":
    expand()
    print("SELF EXPANSION UPDATED")
