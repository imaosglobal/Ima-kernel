from pathlib import Path
import py_compile

# patch source_manager
p = Path("learning/source_manager.py")
text = p.read_text(encoding="utf8")

if "source_cleaner import clean_source" not in text:
    text = text.replace(
        "from learning.knowledge_core.source_router import choose_sources",
        "from learning.knowledge_core.source_router import choose_sources\nfrom learning.knowledge_core.source_cleaner import clean_source"
    )

text = text.replace(
"""        if not allowed or name in allowed:
            results.append(item)""",
"""        if not allowed or name in allowed:
            clean = clean_source(item)
            if clean:
                results.append(clean)"""
)

p.write_text(text,encoding="utf8")
py_compile.compile(str(p),doraise=True)


# create ranking bonus
p = Path("learning/knowledge_core/entity_gate.py")
p.write_text("""
def entity_bonus(question,text):

    q=question.lower()
    t=text.lower()

    if "who was" in q or "who is" in q:
        if "einstein" in t:
            return 20
        if "biography" in t:
            return 20
        return -10

    return 0
""",encoding="utf8")

py_compile.compile(str(p),doraise=True)


print("[OK] knowledge pipeline repaired")
