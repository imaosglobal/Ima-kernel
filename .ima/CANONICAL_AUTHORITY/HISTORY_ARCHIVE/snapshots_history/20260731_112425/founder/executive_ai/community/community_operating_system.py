from founder.executive_ai.community.developer_profile import create_profile
from founder.executive_ai.community.trust_v2 import calculate
from founder.executive_ai.community.role_engine import role_from_trust
from founder.executive_ai.community.permission_engine import permissions
from founder.executive_ai.community.production.audit_log import record


def process_community_action(
    member_id,
    name,
    platform,
    action
):

    profile = create_profile(
        member_id,
        name
    )

    profile["contributions"] = 1

    if "validated" in action:
        profile["validated_lessons"] = 1

    trust = calculate(profile)

    role = role_from_trust(
        trust
    )

    access = permissions(
        role
    )

    audit = record(
        "community_action",
        {
            "member":member_id,
            "platform":platform,
            "action":action,
            "trust":trust,
            "role":role
        }
    )

    return {

        "member":member_id,

        "platform":platform,

        "trust":trust,

        "role":role,

        "permissions":access,

        "audit":audit,

        "status":"processed"

    }
