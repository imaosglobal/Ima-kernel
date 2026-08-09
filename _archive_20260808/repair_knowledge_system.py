from pathlib import Path
import json
import shutil
import time

print("=== IMA KNOWLEDGE REPAIR ===")

# backup
src = Path("engines/knowledge_engine.py")
backup = f"engines/knowledge_engine_backup_{int(time.time())}.py"
shutil.copy(src, backup)

# repair empty json files
for f in Path("knowledge").rglob("*.json"):
    try:
        txt = f.read_text(encoding="utf-8").strip()

        if not txt:
            print("EMPTY:", f)
            f.write_text("{}\n", encoding="utf-8")
            continue

        json.loads(txt)

    except Exception as e:
        print("BROKEN:", f, e)
        f.write_text("{}\n", encoding="utf-8")


# replace search engine
code = r'''
import json
from pathlib import Path

KNOWLEDGE_DIR = Path("knowledge")

STOP_WORDS = {
    "מה","זה","זאת","של","על","את","לי",
    "הסבר","תסביר","איך","האם"
}


def flatten(obj, prefix=""):

    result=[]

    if isinstance(obj,dict):
        for k,v in obj.items():
            result += flatten(v,prefix+" "+str(k))

    elif isinstance(obj,list):
        for x in obj:
            result += flatten(x,prefix)

    else:
        result.append(prefix+" "+str(obj))

    return result



def load_knowledge():

    data=[]

    for f in KNOWLEDGE_DIR.rglob("*.json"):

        try:
            obj=json.loads(
                f.read_text(encoding="utf-8")
            )

            for item in flatten(obj):
                data.append(item)

        except:
            pass

    return data



def search_knowledge(question):

    words=[
        w.lower()
        for w in question.split()
        if w not in STOP_WORDS
    ]

    best=None
    best_score=0

    for text in load_knowledge():

        t=text.lower()

        score=sum(
            1 for w in words
            if w in t
        )

        if score>best_score:
            best_score=score
            best=text


    if best_score>0:

        return {
            "category":"knowledge",
            "answer":best
        }

    return None
'''

src.write_text(code,encoding="utf-8")

print("BACKUP:",backup)
print("KNOWLEDGE REPAIR COMPLETE")
