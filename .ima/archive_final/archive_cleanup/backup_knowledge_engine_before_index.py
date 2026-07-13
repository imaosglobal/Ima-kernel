from pathlib import Path
import json

KNOWLEDGE_ROOT = Path("knowledge")


def load_all_knowledge():
    knowledge = {}

    for file in KNOWLEDGE_ROOT.rglob("*.json"):
        try:
            data = json.loads(
                file.read_text(encoding="utf-8")
            )

            if isinstance(data, dict):
                knowledge.update(data)

        except Exception:
            pass

    return knowledge


def search_knowledge(question):
    knowledge = load_all_knowledge()

    q = question.lower()

    for key, value in knowledge.items():
        if key.lower() in q:
            return value

    return None


def knowledge_topics():
    return list(load_all_knowledge().keys())
