
from pathlib from learning.sources.html_extractor import extract_text
import Path
import json
import time

STORE = Path("learning/world_knowledge_store.json")

def load_store():
    if STORE.exists():
        return json.loads(STORE.read_text(encoding="utf8"))
    return {}

def save_store(data):
    STORE.write_text(
        json.dumps(data,ensure_ascii=False,indent=2),
        encoding="utf8"
    )

def learn_unknown(question):
    store = load_store()

    if question in store:
        return store[question]

    # מקום חיבור עתידי:
    # API / מסמכים / מאגרי ידע / מודלים חיצוניים

    result = {
        "question": question,
        "content": "נדרש מקור ידע חיצוני",
        "source": "expansion_queue",
        "confidence": 0.0,
        "created": time.time()
    }

    store[question] = result
    save_store(store)

    return result
