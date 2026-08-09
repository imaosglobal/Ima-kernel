import json
from pathlib import Path
from datetime import datetime


BASE = Path(__file__).parent.parent

CONCEPTS = BASE / "knowledge/concepts_memory.json"
COMPRESSED = BASE / "knowledge/compressed_memory.json"
ARCHIVE = BASE / "knowledge/archive_memory.json"


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


def calculate_weight(item):

    confidence=item.get(
        "confidence",
        0
    )

    learned=item.get(
        "learned_from",
        1
    )

    return min(
        1.0,
        confidence +
        (learned * 0.03)
    )


def compress():

    concepts=load(CONCEPTS)

    compressed={}
    archive={}


    for name,item in concepts.items():

        weight=calculate_weight(item)

        record={
            "concept":name,
            "confidence":item.get(
                "confidence",
                0
            ),
            "sources":item.get(
                "sources",
                []
            ),
            "weight":weight,
            "compressed_at":
            datetime.now().isoformat()
        }


        if weight >= 0.8:

            compressed[name]=record

        else:

            archive[name]=record


    save(
        COMPRESSED,
        compressed
    )

    save(
        ARCHIVE,
        archive
    )


if __name__=="__main__":

    compress()

    print(
        "KNOWLEDGE COMPRESSED"
    )
