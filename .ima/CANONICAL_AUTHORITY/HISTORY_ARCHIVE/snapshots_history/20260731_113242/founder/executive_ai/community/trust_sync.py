from founder.executive_ai.community.unified_crm import load


def calculate_community_health():

    data=load()

    return {

        "members":
            len(data.get("people",[])),

        "contributions":
            len(data.get("contributions",[])),

        "status":
            "active"

    }
