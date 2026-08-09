from founder.executive_ai.community.unified_crm import (
    link_person,
    add_contribution
)


def sync_community_member(identity, contribution):

    person=link_person(identity)

    add_contribution(
        person["id"],
        contribution
    )

    return {
        "status":"synced",
        "person":person
    }
