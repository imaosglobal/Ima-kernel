import json
from pathlib import Path

FILE=Path("founder/data/founder_context.json")


def save_context(context):

    FILE.write_text(
        json.dumps(
            context,
            ensure_ascii=False,
            indent=2
        )
    )

    return context


def get_context():

    if FILE.exists():
        return json.loads(FILE.read_text())

    return {}
