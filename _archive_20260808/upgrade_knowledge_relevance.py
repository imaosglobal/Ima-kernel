from pathlib import Path
import py_compile

p=Path("learning/knowledge_core/orchestrator.py")

p.write_text("""
from .ranking import rank
from .truth_gate import validate


def relevance(question, text):
    q=set(question.lower().split())
    t=set(text.lower().split())

    if not q or not t:
        return 0

    return len(q.intersection(t)) / len(q)


def answer(question, sources):

    ranked=[]

    for s in sources:

        text=s.get("content","")

        if not validate(text):
            continue

        score=rank(
            s.get("source")
        )

        score += relevance(
            question,
            text[:2000]
        ) * 10

        ranked.append({
            "text":text,
            "source":s.get("source"),
            "score":score
        })


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
        "confidence":round(ranked[0]["score"],2)
    }
""",encoding="utf8")


py_compile.compile(
    str(p),
    doraise=True
)

