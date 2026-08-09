
from learning.knowledge_answer_builder import build_answer

def get_knowledge_answer(brain_result, question):

    if not brain_result:
        return None

    try:
        return build_answer(
            brain_result,
            question
        )
    except Exception:
        return None
