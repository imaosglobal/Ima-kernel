from founder.executive_ai.action_engine.executors.lead_finder import find_leads
from founder.executive_ai.action_engine.executors.lead_ranker import rank_leads
from founder.executive_ai.action_engine.executors.outreach_creator import create_messages
from founder.executive_ai.action_engine.executors.feedback_collector import collect_feedback
from founder.executive_ai.action_engine.executors.outbound_gateway import execute_outreach



def _prepare_public_impact_message(context):
    target = str(context.get("target", "organization"))
    return {
        "action": "prepare_public_impact_message",
        "target": target,
        "status": "message_ready",
        "message": (
            f"IMA prepared a public-impact message for {target}"
        ),
        "external_action": False,
    }


def _monitor(context):
    target = str(context.get("target", "organization"))
    return {
        "action": "monitor",
        "target": target,
        "status": "monitoring",
        "external_action": False,
    }


EXECUTORS = {
    "find_leads": find_leads,
    "rank_leads": rank_leads,
    "generate_outreach": create_messages,
    "create_personal_outreach": execute_outreach,
    "collect_feedback": collect_feedback,
    "prepare_public_impact_message": _prepare_public_impact_message,
    "monitor": _monitor,

}



def execute_action(action, context={}):

    executor=EXECUTORS.get(action)

    if not executor:
        return {
            "error":"unknown action",
            "action":action
        }

    return executor(context)
