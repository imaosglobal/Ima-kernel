from pathlib import Path
import json

KNOWLEDGE_ROOT = Path("knowledge")
INDEX_FILE = Path("knowledge/index/categories.json")


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


def load_categories():
    try:
        return json.loads(
            INDEX_FILE.read_text(encoding="utf-8")
        )
    except Exception:
        return {}


def find_category(term):
    categories = load_categories()

    for category, words in categories.items():
        if term in words:
            return category

    return None


def search_knowledge(question):

    knowledge = load_all_knowledge()
    q = question.lower()

    for key, value in knowledge.items():
        if key.lower() in q:
            category = find_category(key)

            return {
                "answer": value,
                "topic": key,
                "category": category
            }

    return None


def knowledge_topics():
    return list(load_all_knowledge().keys())
