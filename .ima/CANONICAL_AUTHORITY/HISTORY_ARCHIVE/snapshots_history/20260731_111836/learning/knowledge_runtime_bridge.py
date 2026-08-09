
from learning.source_manager import collect
from learning.knowledge_core.source_router import choose_sources
from learning.knowledge_core.orchestrator import answer


def ask_knowledge(question, memory=None):

    route = choose_sources(question)
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
