from founder.executive_ai.global_intelligence.world_adapters import real_world_scanner


from founder.executive_ai.global_intelligence.opportunity_engine import evaluate_world
from founder.executive_ai.action_engine.feedback_engine import analyze_feedback


def generate_actions():

    real_signals = real_world_scanner.scan()



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

            target = str(r.get("target") or "").lower()

            target_words = [
                w for w in target.split()
                if len(w) > 3
            ]

            matches = [
                w for w in target_words
                if w in name.lower()
            ]

            if len(matches) >= 2:

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
