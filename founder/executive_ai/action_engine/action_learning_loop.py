from founder.executive_ai.action_engine.feedback_engine import analyze_feedback
from founder.executive_ai.action_engine.action_memory import get_actions


def learning_cycle():

    actions=get_actions()
    feedback=analyze_feedback()

    return {
        "actions_seen":len(actions),
        "feedback":feedback,
        "learning_state":
            "IMA updating strategy from results"
    }
