from founder.executive_ai.community.global_connector_engine import receive_message
from founder.executive_ai.community.contribution_queue import add_proposal
from founder.executive_ai.community.change_sandbox import evaluate
from founder.executive_ai.community.core_learning_bridge import accept_validated_learning
from founder.executive_ai.community.crm_bridge import sync_community_member


def process_external_signal(platform, user, message):

    incoming = receive_message(
        platform,
        user,
        message
    )

    proposal = add_proposal(
        platform,
        message
    )

    analysis = evaluate(
        proposal
    )

    return {
        "incoming": incoming,
        "proposal": proposal,
        "sandbox": analysis,
        "status": "awaiting_validation"
    }


def promote_learning(proposal):

    proposal["status"]="validated"

    return accept_validated_learning(
        proposal
    )
