from founder.executive_ai.community.unified_crm import (
    link_person,
    add_contribution
)


def process_community_event(
    user_id,
    name,
    source,
    contribution
):

    identity={
        "id":user_id,
        "name":name
    }

    person=link_person(
        identity,
        source
    )

    event=add_contribution(
        user_id,
        contribution
    )

    return {
        "status":"crm_updated",
        "person":person,
        "event":event
    }
