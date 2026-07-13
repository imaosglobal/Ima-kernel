
import json
import os
from pathlib import Path


KNOWLEDGE_DIR = Path("knowledge")


def load_all_knowledge():

    database = []

    if not KNOWLEDGE_DIR.exists():
        return database

    for file in KNOWLEDGE_DIR.rglob("*.json"):

        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)

            database.append({
                "file": str(file),
                "data": data
            })

        except Exception:
            continue

    return database



def flatten(obj, prefix=""):

    result=[]

    if isinstance(obj, dict):
        for k,v in obj.items():
            result.extend(flatten(v, prefix + " " + str(k)))

    elif isinstance(obj, list):
        for item in obj:
            result.extend(flatten(item, prefix))

    else:
        result.append(prefix + " " + str(obj))

    return result



def search_knowledge(question):

    question = question.lower()

    db = load_all_knowledge()

    best = None
    score = 0

    for item in db:

        texts = flatten(item["data"])

        for text in texts:

            t=text.lower()

            current=sum(
                1 for word in question.split()
                if word in t
            )

            if current > score:
                score=current
                best=text


    if best:
        return {
            "category":"knowledge",
            "answer":best
        }

    return None
