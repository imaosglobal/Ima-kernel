import json
from pathlib import Path

FILE = Path(
    "learning/sources/candidates.json"
)


def update_candidate(updated):

    data=json.loads(
        FILE.read_text(
            encoding="utf8"
        )
    )

    for i,c in enumerate(data):
        if (
            c.get("name")
            ==
            updated.get("name")
        ):
            data[i]=updated

    FILE.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf8"
    )
