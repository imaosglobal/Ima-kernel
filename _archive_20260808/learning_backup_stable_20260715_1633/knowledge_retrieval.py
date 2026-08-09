
from pathlib import Path
import json

STORE = Path("learning/knowledge_store.json")

def retrieve(query):

    try:
        data=json.loads(
            STORE.read_text(encoding="utf8")
        )

        for key,value in data.items():
            if key in query:
                return value

    except Exception:
        return None

    return None
