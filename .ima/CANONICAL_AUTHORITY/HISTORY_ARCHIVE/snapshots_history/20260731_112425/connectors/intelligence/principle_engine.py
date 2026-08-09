import json
from pathlib import Path
from datetime import datetime


BASE = Path(__file__).parent.parent

GRAPH = BASE / "knowledge/universal_graph/knowledge_graph.json"


def load():
    return json.loads(
        GRAPH.read_text()
    )


def save(data):
    GRAPH.write_text(
        json.dumps(
            data,
            indent=2,
            ensure_ascii=False
        )
    )


def generate():

    data=load()

    principles=data.setdefault(
        "principles",
        {}
    )


    patterns=data.get(
        "patterns",
        {}
    )


    if "business_system" in patterns:

        principles["resource_flow"]={
            "derived_from":
            "business_system",

            "statement":
            "מערכת מנהלת זרימת משאבים בין אנשים, נכסים ותהליכים",

            "confidence":0.8,

            "created":
            datetime.now().isoformat()
        }


    if "human_system" in patterns:

        principles["human_learning"]={
            "derived_from":
            "human_system",

            "statement":
            "מערכת חיה מתפתחת דרך זהות, רגש, החלטה ולמידה",

            "confidence":0.8,

            "created":
            datetime.now().isoformat()
        }


    save(data)


if __name__=="__main__":

    generate()

    print(
        "PRINCIPLES GENERATED"
    )
