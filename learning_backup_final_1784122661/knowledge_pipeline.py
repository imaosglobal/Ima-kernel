import json

from learning.knowledge_graph_retrieval import search_concept
from learning.knowledge_answer_builder import build_answer
from learning.knowledge_expansion_engine import expand_knowledge


def run_knowledge_pipeline(message):

    try:
        nodes = search_concept(message)

        if nodes:
            return {
                "type":"graph",
                "answer":build_answer(
                    {
                    "domain":"knowledge_graph",
                    "content":json.dumps(
                        nodes,
                        ensure_ascii=False
                    )
                    },
                    message
                ),
                "nodes":nodes
            }

    except Exception:
        pass


    try:
        expansion = expand_knowledge(message)

        if expansion:
            return {
                "type":"expansion",
                "answer":expansion.get("content",""),
                "expansion":expansion
            }

    except Exception:
        pass


    return None
