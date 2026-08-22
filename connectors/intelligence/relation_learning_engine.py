import json
from pathlib import Path
from datetime import datetime


BASE = Path(__file__).parent.parent

GRAPH = BASE / "knowledge/universal_graph/knowledge_graph.json"


def load():
    if GRAPH.exists():
        return json.loads(
            GRAPH.read_text()
        )
    return {}


def save(data):
    GRAPH.write_text(
        json.dumps(
            data,
            indent=2,
            ensure_ascii=False
        )
    )


def learn_relations():

    graph = load()

    relations = graph.setdefault(
        "relations",
        {}
    )

    concepts = graph.get(
        "concepts",
        {}
    )


    rules = [

        (
            "inventory",
            "sales",
            "resource_dependency"
        ),

        (
            "sales",
            "accounting",
            "financial_flow"
        ),

        (
            "customers",
            "marketing",
            "engagement_flow"
        ),

        (
            "identity",
            "emotion",
            "human_interaction"
        ),

        (
            "emotion",
            "music",
            "expression"
        ),

        (
            "learning",
            "decision",
            "adaptation"
        )
    ]


    for a,b,kind in rules:

        if (
            a in concepts
            or a in str(graph)
        ) and (
            b in concepts
            or b in str(graph)
        ):

            key=f"{a}->{b}"

            relations[key]={
                "type":kind,
                "confidence":0.8,
                "updated":
                datetime.now().isoformat()
            }


    save(graph)


if __name__=="__main__":
    learn_relations()
