import json
from pathlib import Path
from datetime import datetime


BASE = Path(__file__).parent.parent

GRAPH = BASE / "knowledge/universal_graph/knowledge_graph.json"
MEMORY = Path.home() / ".ima/memory"


def load(path):
    if path.exists():
        return json.loads(path.read_text())
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


def build_resolution():

    graph = load(GRAPH)

    resolution = {
        "updated": datetime.now().isoformat(),

        "layers": {

            "details": {
                "count":
                len(graph.get("concepts",{}))
            },

            "concepts": list(
                graph.get("concepts",{}).keys()
            ),

            "patterns": list(
                graph.get("patterns",{}).keys()
            ),

            "principles": list(
                graph.get("principles",{}).keys()
            )
        }
    }


    save(
        MEMORY / "memory_resolution.json",
        resolution
    )


if __name__=="__main__":

    build_resolution()

    print(
        "MEMORY RESOLUTION UPDATED"
    )
