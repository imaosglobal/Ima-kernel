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

    if "explain" in q:
        return "explanation"

    if "what is" in q:
        return "definition"

    return "general"


def score_source(question, source, text):

    score = rank(source)

    qtype = detect_type(question)
    t = text.lower()

    if qtype == "person":

        if source in ["arXiv","Nature","IEEE","PubMed"]:
            score -= 20

        if any(x in t for x in [
            "born",
            "died",
            "physicist",
            "biography",
            "einstein"
        ]):
            score += 20


    if qtype == "explanation":

        if len(text) > 500:
            score += 5

        if source in ["arXiv","IEEE"]:
            if any(x in t for x in [
                "algorithm",
                "framework",
                "dataset",
                "architecture"
            ]):
                score -= 5


    if qtype == "definition":

        if any(x in t for x in [
            "is the",
            "refers to",
            "capability",
            "defined"
        ]):
            score += 10


    return score



def answer(question, sources):

    ranked=[]

    for s in sources:

        text=s.get("content","")

        if not validate(text):
            continue

        score=score_source(
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

""", encoding="utf8")


py_compile.compile(
    str(p),
    doraise=True
)

