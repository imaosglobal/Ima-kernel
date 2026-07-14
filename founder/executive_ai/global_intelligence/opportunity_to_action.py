from founder.executive_ai.global_intelligence.opportunity_engine import evaluate_world


def generate_actions():

    world=evaluate_world()

    actions=[]

    for item in world["opportunities"]:

        entity=item["entity"]

        if item["opportunity_score"] >= 60:

            actions.append({
                "target":entity["name"],
                "type":entity["type"],
                "country":entity.get("country","unknown"),
                "action":"create_personal_outreach",
                "priority":"high",
                "reason":item["reasoning"]
            })

        else:

            actions.append({
                "target":entity["name"],
                "type":entity["type"],
                "country":entity.get("country","unknown"),
                "action":"monitor",
                "priority":"medium",
                "reason":item["reasoning"]
            })

    return actions
