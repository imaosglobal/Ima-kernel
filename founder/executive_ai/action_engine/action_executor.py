from founder.executive_ai.action_engine.executors.lead_finder import find_leads
from founder.executive_ai.action_engine.executors.lead_ranker import rank_leads
from founder.executive_ai.action_engine.executors.outreach_creator import create_messages
from founder.executive_ai.action_engine.executors.feedback_collector import collect_feedback
from founder.executive_ai.action_engine.feedback_engine import analyze_feedback


def create_personal_outreach(context):
    """
    Prepare personalized outreach.
    Sending remains explicitly approval-gated.
    """
    return {
        "status": "approval_required",
        "action": "create_personal_outreach",
        "reason": "external communication requires explicit approval",
        "target": context.get("target"),
        "score": context.get("score"),
        "context": context,
    }


def send_outreach(context):
    """
    External communication is approval-gated.
    Never send automatically.
    """
    return {
        "status": "approval_required",
        "action": "send_outreach",
        "reason": "external communication requires explicit approval",
        "context": context,
    }


def update_product(context):
    """
    Product changes are proposal-only until explicitly approved.
    """
    return {
        "status": "product_update_proposed",
        "action": "update_product",
        "context": context,
    }


def prepare_public_impact_message(context):
    """
    Prepare a public-impact message without publishing or sending it.
    """
    target = context.get(
        "target",
        "organization",
    )

    return {
        "status": "message_ready",
        "action": "prepare_public_impact_message",
        "target": target,
        "strategy": "public impact focused outreach",
        "external_side_effect": False,
    }


def monitor(context):
    """
    Monitoring is observational and has no external side effect.
    """
    return {
        "status": "monitoring",
        "action": "monitor",
        "target": context.get("target"),
        "score": context.get("score"),
        "external_side_effect": False,
    }


EXECUTORS = {
    "find_leads": find_leads,
    "rank_leads": rank_leads,
    "generate_outreach": create_messages,
    "collect_feedback": collect_feedback,
    "analyze_feedback": lambda context: analyze_feedback(),
    "create_personal_outreach": create_personal_outreach,
    "send_outreach": send_outreach,
    "update_product": update_product,

    # World-intelligence actions
    "prepare_public_impact_message": prepare_public_impact_message,
    "monitor": monitor,
}


def execute_action(action, context=None):

    if context is None:
        context = {}

    executor = EXECUTORS.get(action)

    if not executor:
        return {
            "status": "unknown_action",
            "action": action,
        }

    try:
        result = executor(context)

        return {
            "status": "executed",
            "action": action,
            "result": result,
        }

    except Exception as exc:

        return {
            "status": "execution_failed",
            "action": action,
            "error": repr(exc),
        }
