from pathlib import Path
import py_compile

p=Path("learning/knowledge_core/orchestrator.py")

text=p.read_text(encoding="utf8")

text=text.replace(
    r'\n\n        score += relevance(',
    '\n\n        score += relevance('
)

text=text.replace(
    '\\n\\n        score += relevance(',
    '\n\n        score += relevance('
)

p.write_text(text,encoding="utf8")

py_compile.compile(
    str(p),
    doraise=True
)

print("[OK] orchestrator syntax fixed")
