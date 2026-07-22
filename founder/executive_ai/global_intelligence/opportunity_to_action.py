
from founder.executive_ai.global_intelligence.opportunity_engine import evaluate_world
from founder.executive_ai.action_engine.feedback_engine import analyze_feedback


def generate_actions():

    world = evaluate_world()

    feedback = analyze_feedback()

    records = feedback.get("records", [])

    actions=[]


    for item in world.get("top_opportunities", []):

        entity=item.get("entity",{})
        score=item.get("opportunity_score",0)

        name=entity.get("name","")

        entity_type=entity.get("type")


        previous_failure=False

        for r in records:
            if r.get("target","").lower() in name.lower():
                if r.get("status") in [
                    "no_response",
                    "failed"
                ]:
                    previous_failure=True


        if entity_type=="government" and previous_failure:

            actions.append({
                "action":"prepare_public_impact_message",
                "target":name,
                "reason":"government learning adjustment",
                "score":score
            })


        elif score >= 50:

            actions.append({
                "action":"create_personal_outreach",
                "target":name,
                "reason":"high opportunity score",
                "score":score,
                "signals":item.get("signals",[])
            })


        else:

            actions.append({
                "action":"monitor",
                "target":name,
                "reason":"below action threshold",
                "score":score
            })


    return actions
