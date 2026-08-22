from pathlib import Path
import py_compile

p=Path("learning/knowledge_core/orchestrator.py")

text=p.read_text(encoding="utf8")

insert = '''

def content_penalty(question, source, text):

    q=question.lower()
    t=text.lower()

    penalty=0

    # שאלות על אנשים
    if "who was" in q or "who is" in q:

        if source in ["arXiv","Nature","IEEE","PubMed"]:
            penalty -= 20

        if any(x in t for x in [
            "mcmc",
            "algorithm",
            "framework",
            "regression",
            "dataset"
        ]):
            penalty -= 30


    # שאלות הסבר
    if "explain" in q:

        if source in ["arXiv","IEEE"]:
            if "framework" in t or "algorithm" in t:
                penalty -= 10


    return penalty

'''

text=text.replace(
"def answer(question, sources):",
insert+"\ndef answer(question, sources):"
)

text=text.replace(
"score += relevance_bonus(",
"score += content_penalty(question, s.get(\"source\"), text)\\n\\n        score += relevance_bonus("
)

p.write_text(text,encoding="utf8")

py_compile.compile(
    str(p),
    doraise=True
)

