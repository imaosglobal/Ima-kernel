from pathlib import Path
import py_compile

p=Path("learning/knowledge_core/orchestrator.py")

p.write_text("""
from .ranking import rank
from .truth_gate import validate


def detect_type(question):
    q=question.lower()

    if "who was" in q or "who is" in q:
        return "person"

    if "what is" in q:
        return "definition"

    if "explain" in q:
        return "explanation"

    return "general"


def relevance_bonus(question, source, text):

    qtype=detect_type(question)
    t=text.lower()

    score=0

    if qtype=="person":
        if any(x in t for x in [
            "born",
            "died",
            "biography",
            "physicist",
            "einstein"
        ]):
            score += 20

        if source in [
            "Wikipedia",
            "Britannica",
            "DuckDuckGo"
        ]:
            score += 15


    if qtype=="definition":
        if any(x in t for x in [
            "is the",
            "refers to",
            "defined as",
            "capability"
        ]):
            score += 10


    if qtype=="explanation":
        if len(text)>500:
            score += 5


    return score



def answer(question, sources):

    ranked=[]

    for s in sources:

        text=s.get("content","")

        if not validate(text):
            continue

        score=rank(
            s.get("source")
        )

        score += relevance_bonus(
            question,
            s.get("source"),
            text
        )

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

