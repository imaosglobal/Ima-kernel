
from .context import build_context
from learning.sources.html_extractor import extract_text
from .confidence import score_answer
from .deduplicator import clean_duplicates

def query(question, memory=None, sources=None):
    context=build_context(question,memory)

    answers=[]

    if sources:
        for s in sources:
            if s.get("content"):
                content = s.get("content","")

                if "<html" in content.lower() or "<!doctype" in content.lower():
                    content = extract_text(content)

                s["content"] = content
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
