from founder.executive_ai.action_engine.executors.lead_finder import find_leads
from founder.executive_ai.action_engine.executors.lead_ranker import rank_leads
from founder.executive_ai.action_engine.executors.outreach_creator import create_messages
from founder.executive_ai.action_engine.executors.feedback_collector import collect_feedback


EXECUTORS={

    "find_leads":find_leads,

    "rank_leads":rank_leads,

    "generate_outreach":create_messages,

    "collect_feedback":collect_feedback

}


def execute_action(action, context={}):

    executor=EXECUTORS.get(action)

    if not executor:
        return {
            "error":"unknown action",
            "action":action
        }

    return executor(context)
