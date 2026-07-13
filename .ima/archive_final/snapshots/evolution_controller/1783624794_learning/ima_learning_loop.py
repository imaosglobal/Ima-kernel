from learning.learning_scheduler import learning_cycle
from learning.knowledge_expander import expand_knowledge
from learning.self_reflection import add_lesson
from learning.decision_engine import make_learning_decision
from learning.adaptive_loop import run_adaptive_cycle
from learning.self_manager import manage_learning
from learning.feedback_planner import generate_feedback_improvements
from learning.meta_orchestrator import run_meta_analysis
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

    meta = run_meta_analysis()

    feedback_cycle = generate_feedback_improvements()

    return {
        "cycle": cycle,
        "learned": learned,
        "adaptive": adaptive,
        "management": management,
        "meta": meta,
        "feedback_cycle": feedback_cycle,
        "status": "IMA autonomous learning cycle finished"
    }
