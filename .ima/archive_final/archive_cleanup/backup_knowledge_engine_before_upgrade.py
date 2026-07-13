
import json
from pathlib import Path

KNOWLEDGE_PATH = Path("knowledge")


def load_domain(domain):
    file = KNOWLEDGE_PATH / f"{domain}.json"

    if not file.exists():
        return {}

    try:
        return json.loads(
            file.read_text(encoding="utf-8")
        )
    except:
        return {}


def search_knowledge(question):

    q = question.lower()

    results = []

    for file in KNOWLEDGE_PATH.glob("*.json"):

        try:
            data = json.loads(
                file.read_text(encoding="utf-8")
            )

            text = json.dumps(
                data,
                ensure_ascii=False
            )

            for key, value in data.get("concepts", {}).items():

                if key.lower() in q:
                    results.append(value)

        except:
            continue

    if results:
        return "\n\n".join(results)

    return None
