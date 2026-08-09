from founder.executive_ai.self_learning_core.self_audit import audit
from founder.executive_ai.self_learning_core.improvement_engine import generate_improvements

def run_learning_cycle():

    return {
        "audit": audit(),
        "improvements": generate_improvements()
    }

def run():

    return run_learning_cycle()
