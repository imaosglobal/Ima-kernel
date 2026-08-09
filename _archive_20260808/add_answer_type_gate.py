from pathlib import Path
import py_compile

p=Path("learning/knowledge_core/orchestrator.py")

text=p.read_text(encoding="utf8")

text=text.replace(
"def relevance(question, text):",
'''
def answer_type_bonus(question, source, text):

    q=question.lower()
    t=text.lower()

    bonus=0

    if "who was" in q:
        if any(x in t for x in [
            "born",
            "died",
            "physicist",
            "biography",
            "einstein"
        ]):
            bonus += 8

    if "what is" in q:
        if any(x in t for x in [
            "is defined",
            "refers to",
            "capability",
            "system"
        ]):
            bonus += 5

    if "explain" in q:
        if len(text)>1000:
            bonus += 3

    return bonus


def relevance(question, text):
'''
)

text=text.replace(
"score += relevance(",
"score += answer_type_bonus(question, s.get(\"source\"), text)\\n\\n        score += relevance("
)

p.write_text(text,encoding="utf8")

py_compile.compile(
    str(p),
    doraise=True
)

print("[OK] answer type gate added")
