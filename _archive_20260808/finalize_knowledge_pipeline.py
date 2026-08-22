from pathlib import Path
import py_compile

p=Path("learning/knowledge_runtime_bridge.py")

p.write_text("""
from learning.source_manager import collect
from learning.knowledge_core.orchestrator import answer


def ask_knowledge(question, memory=None):

    sources = collect(question)

    result = answer(
        question,
        sources
    )

    return {
        "answer": result.get("answer"),
        "source": result.get("source"),
        "confidence": result.get("confidence"),
        "context": {
            "question": question,
            "memory_used": bool(memory)
        },
        "sources": sources
    }
""", encoding="utf8")

py_compile.compile(
    "learning/knowledge_runtime_bridge.py",
    doraise=True
)




from learning.knowledge_runtime_bridge import ask_knowledge

r=ask_knowledge(
    "What is artificial intelligence?"
)


