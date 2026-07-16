from learning.source_manager import collect
from learning.knowledge_fusion import fuse_sources
from learning.knowledge_compactor import compact

def ask_knowledge(question):
    sources = collect(question)

    for s in sources:
        if "content" in s:
            s["content"] = compact(s["content"])

    if not sources:
        return {
            "answer": None,
            "sources": []
        }

    result = fuse_sources(question, sources)

    if not result:
        return {
            "answer": None,
            "sources": sources
        }

    return {
        "answer": result.get("answer"),
        "source": result.get("source"),
        "confidence": result.get("confidence"),
        "url": result.get("url"),
        "sources": result.get("all_sources", sources)
    }
