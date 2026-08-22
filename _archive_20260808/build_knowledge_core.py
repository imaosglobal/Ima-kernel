from pathlib import Path
import json

base=Path("learning/knowledge_core")
base.mkdir(parents=True,exist_ok=True)

files={
"core.py":'''
from .context import build_context
from .confidence import score_answer
from .deduplicator import clean_duplicates

def query(question, memory=None, sources=None):
    context=build_context(question,memory)

    answers=[]

    if sources:
        for s in sources:
            if s.get("content"):
                answers.append(s)

    answers=clean_duplicates(answers)

    best=None
    score=0

    for a in answers:
        s=score_answer(a)
        if s>score:
            score=s
            best=a

    return {
        "answer": best.get("content") if best else None,
        "confidence":score,
        "context":context
    }
''',

"context.py":'''
def build_context(question,memory=None):
    return {
        "question":question,
        "memory_used":bool(memory)
    }
''',

"confidence.py":'''
def score_answer(item):
    score=0

    score+=item.get("confidence",0)

    source=item.get("source","")

    if source in ["Wikipedia","Nature","NASA","PubMed"]:
        score+=1

    return score
''',

"deduplicator.py":'''
def clean_duplicates(items):
    seen=set()
    result=[]

    for x in items:
        key=x.get("content","")[:200]

        if key not in seen:
            seen.add(key)
            result.append(x)

    return result
''',

"response_builder.py":'''
def build_response(data):
    return data.get("answer")
'''
}

for name,content in files.items():
    (base/name).write_text(content,encoding="utf8")

