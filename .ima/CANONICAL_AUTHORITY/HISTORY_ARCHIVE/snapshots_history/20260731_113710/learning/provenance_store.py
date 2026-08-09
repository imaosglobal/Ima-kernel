
from learning.sources.html_extractor import extract_text
import json
from pathlib import Path
import time

FILE=Path("learning/provenance_memory.json")

def save_provenance(
    knowledge_id,
    content,
    source,
    validation
):

    data={}

    if FILE.exists():
        data=json.loads(
            FILE.read_text(encoding="utf8")
        )

    data[knowledge_id]={
        "content":content,
        "source":source,
        "validation":validation,
        "stored_at":time.time()
    }

    FILE.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf8"
    )

    return data[knowledge_id]


def get_provenance(knowledge_id):

    if not FILE.exists():
        return None

    data=json.loads(
        FILE.read_text(encoding="utf8")
    )

    return data.get(knowledge_id)
