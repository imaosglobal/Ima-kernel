from founder.executive_ai.memory.memory_ranker import rank_memories
from founder.executive_ai.memory.context_synthesizer import synthesize
from founder.executive_ai.memory.founder_timeline import build_timeline


def enrich_answer(query, memories):

    ranked = rank_memories(
        memories,
        query
    )

    context = synthesize(
        ranked
    )

    timeline = build_timeline()

    return {
        "query": query,
        "memory_context": context,
        "founder_history": timeline[-10:]
    }
