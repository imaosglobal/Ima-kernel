from pathlib import Path
import py_compile

base=Path("learning/knowledge_core")
base.mkdir(parents=True,exist_ok=True)

files={

"truth_gate.py":'''
def validate(answer):
    if not answer:
        return False
    bad=["html","doctype","javascript","stylesheet","cookie"]
    text=str(answer).lower()
    return not any(x in text for x in bad)
''',

"ranking.py":'''
def rank(source):
    weights={
        "arXiv":9,
        "Nature":9,
        "PubMed":8,
        "NASA":8,
        "DuckDuckGo":5
    }
    return weights.get(source,1)
''',

"orchestrator.py":'''
from .ranking import rank
from .truth_gate import validate

def answer(question, sources):

    ranked=[]

    for s in sources:
        text=s.get("content","")
        if validate(text):
            ranked.append(
                {
                "text":text,
                "source":s.get("source"),
                "score":rank(s.get("source"))
                }
            )

    ranked.sort(
        key=lambda x:x["score"],
        reverse=True
    )

    if not ranked:
        return {
        "answer":None,
        "confidence":0
        }

    return {
    "answer":ranked[0]["text"],
    "source":ranked[0]["source"],
    "confidence":ranked[0]["score"]
    }
'''
}

for name,data in files.items():
    p=base/name
    p.write_text(data,encoding="utf8")
    py_compile.compile(str(p),doraise=True)

