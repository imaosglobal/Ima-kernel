from pathlib import Path
import shutil
import time

path = Path("engines/knowledge_engine.py")

backup = f"engines/knowledge_engine_backup_{int(time.time())}.py"
shutil.copy(path, backup)

new_code = r'''
import json
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

        except Exception as e:

    return database



def flatten(obj, prefix=""):

    result=[]

    if isinstance(obj, dict):

        for k,v in obj.items():

            new_prefix = (
                prefix + " " + str(k)
                if prefix
                else str(k)
            )

            result.extend(
                flatten(v,new_prefix)
            )

    elif isinstance(obj,list):

        for item in obj:
            result.extend(
                flatten(item,prefix)
            )

    else:

        result.append(
            prefix + ": " + str(obj)
        )

    return result



def search_knowledge(question):

    words = [
        x.lower()
        for x in question.split()
        if len(x)>1
    ]

    db = load_all_knowledge()

    best=None
    best_score=0

    for item in db:

        for text in flatten(item["data"]):

            t=text.lower()

            score=sum(
                1 for w in words
                if w in t
            )

            if score > best_score:
                best_score=score
                best=text


    if best_score>0:

        return {
            "category":"knowledge",
            "answer":best
        }


    return None
'''

path.write_text(new_code, encoding="utf-8")

