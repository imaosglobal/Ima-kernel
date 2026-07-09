from learning.learning_scheduler import learning_cycle
from learning.knowledge_expander import expand_knowledge
from learning.self_reflection import add_lesson
from learning.decision_engine import make_learning_decision
from learning.adaptive_loop import run_adaptive_cycle
from learning.self_manager import manage_learning
from datetime import datetime


def run_ima_learning_loop():

    cycle = learning_cycle()

    learned = expand_knowledge()

    for item in learned:
        make_learning_decision(
            "knowledge_expansion",
            item
        )

    if learned:
        add_lesson(
            f"מחזור למידה {datetime.now()}: נוספו {len(learned)} תובנות חדשות"
        )

    adaptive = run_adaptive_cycle()

    management = manage_learning()

    return {
        "cycle": cycle,
        "learned": learned,
        "adaptive": adaptive,
        "management": management,
        "status": "IMA autonomous learning cycle finished"
    }
