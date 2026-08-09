from pathlib import Path
import json
from datetime import datetime

BASE=Path.home()/"ima_kernel"

GRAPH=BASE/"connectors/knowledge/universal_graph/knowledge_graph.json"

STATE=Path.home()/".ima/evolution/kernel_knowledge_bridge.json"


def load(path):
    if path.exists():
        try:
            return json.loads(path.read_text())
        except:
            return {}
    return {}


def save(path,data):
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


graph=load(GRAPH)


bridge={

    "generated":
    datetime.now().isoformat(),

    "bridge":
    "knowledge_router_to_kernel",

    "status":
    "CONNECTED",

    "available_knowledge":{

        "domains":
        list(
            graph.get(
                "domains",
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

    "runtime_policy":[

        "read knowledge",

        "select relevant capability",

        "avoid duplicate creation",

        "prefer minimal evolution"

    ]
}


save(
    STATE,
    bridge
)


print("KNOWLEDGE ROUTER CONNECTED")
