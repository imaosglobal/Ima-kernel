from pathlib import Path
import shutil
import time

src=Path("engines/knowledge_engine.py")
backup=f"engines/knowledge_engine_backup_search_{int(time.time())}.py"
shutil.copy(src,backup)

code=r'''
import json
from pathlib import Path

KNOWLEDGE_DIR=Path("knowledge")

STOP_WORDS={
"מה","זה","זאת","מי","הוא","היא",
"של","על","את","לי","איך","הסבר",
"מהו","מי זה","מי היא"
}


def flatten(obj,prefix=""):

    out=[]

    if isinstance(obj,dict):
        for k,v in obj.items():
            out += flatten(v,prefix+" "+str(k))

    elif isinstance(obj,list):
        for x in obj:
            out += flatten(x,prefix)

    else:
        out.append(prefix+" "+str(obj))

    return out



def load_knowledge():

    result=[]

    for f in KNOWLEDGE_DIR.rglob("*.json"):

        try:
            data=json.loads(
                f.read_text(encoding="utf-8")
            )

            result += flatten(data)

        except:
            pass

    return result



def search_knowledge(question):

    q=question.lower()

    words=[
        w for w in q.split()
        if w not in STOP_WORDS and len(w)>1
    ]

    best=None
    best_score=0


    for text in load_knowledge():

        t=text.lower()

        score=0

        for w in words:

            if w in t:
                score+=3

            # התאמה למפתח לפני התוכן
            if t.strip().startswith(w):
                score+=5


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

