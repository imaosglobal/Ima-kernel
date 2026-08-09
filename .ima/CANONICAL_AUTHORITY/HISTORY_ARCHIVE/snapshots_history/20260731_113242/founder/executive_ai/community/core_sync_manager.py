from founder.executive_ai.community.unified_crm import load


def system_status():

    crm=load()

    return {
        "crm_people":len(crm.get("people",[])),
        "communities":len(crm.get("communities",[])),
        "contributions":len(crm.get("contributions",[])),
        "status":"synchronized"
    }
