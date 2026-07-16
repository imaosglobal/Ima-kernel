import json
from pathlib import Path
from datetime import datetime


BASE = Path.home() / "ima_kernel"

IMA = Path.home() / ".ima"


DAILY = BASE / ".ima/daily"
EVOLUTION = BASE / ".ima/evolution"


def load_json(path):

    if path.exists():
        try:
            return json.loads(
                path.read_text()
            )
        except:
            return {}

    return {}


def save_json(path,data):

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    path.write_text(
        json.dumps(
            data,
            indent=2,
            ensure_ascii=False
        )
    )


def build_summary():

    graph = load_json(
        BASE /
        "connectors/knowledge/universal_graph/knowledge_graph.json"
    )


    summary={

        "date":
        datetime.now().isoformat(),

        "system":
        "IMA",

        "created_today":[
            "software intelligence",
            "universal knowledge graph",
            "pattern engine",
            "principle engine",
            "compression engine",
            "self expansion engine",
            "relation learning engine"
        ],


        "current_understanding":{

            "domains":
            list(
                graph.get(
                    "domains",
                    {}
                ).keys()
            ),

            "patterns":
            list(
                graph.get(
                    "patterns",
                    {}
                ).keys()
            ),

            "principles":
            list(
                graph.get(
                    "principles",
                    {}
                ).keys()
            ),

            "relations":
            list(
                graph.get(
                    "relations",
                    {}
                ).keys()
            )
        },


        "next_session":[

            "connect kernel to knowledge router",

            "build self analysis",

            "improve autonomous planning",

            "continue universal learning"
        ]
    }


    today=DAILY / (
        datetime.now()
        .strftime("%Y-%m-%d.json")
    )

    save_json(
        today,
        summary
    )


    with open(
        EVOLUTION /
        "learning_history.jsonl",
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            json.dumps(
                summary,
                ensure_ascii=False
            )
            + "\n"
        )


    save_json(
        DAILY /
        "current_state.json",
        summary
    )


if __name__=="__main__":

    build_summary()

    print(
        "IMA DAILY EVOLUTION SAVED"
    )
    import os
    os.system(
        "python system_truth_layer.py"
    )"
    )

    import os

    os.system(
        "python daily_evolution_scheduler.py"
    )
