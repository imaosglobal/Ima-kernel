from learning.learning_scheduler import learning_cycle
from learning.knowledge_expander import expand_knowledge
from learning.self_reflection import add_lesson
from datetime import datetime


def run_ima_learning_loop():

    cycle = learning_cycle()

    learned = expand_knowledge()

    if learned:
        add_lesson(
            f"מחזור למידה {datetime.now()}: נוספו {len(learned)} תובנות חדשות"
        )

    return {
        "cycle": cycle,
        "learned": learned,
        "status": "IMA autonomous learning cycle finished"
    }
