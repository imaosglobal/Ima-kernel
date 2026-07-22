
from founder.executive_ai.global_intelligence.opportunity_engine import evaluate_world


def generate_actions():

    world = evaluate_world()

    actions = []

    for item in world.get("top_opportunities", []):

        score = item.get("opportunity_score",0)
        entity = item.get("entity",{})

        if score >= 50:
            actions.append({
                "action":"create_personal_outreach",
                "target":entity.get("name"),
                "reason":"high opportunity score",
                "score":score,
                "signals":item.get("signals",[])
            })

        elif score >= 30:
            actions.append({
                "action":"monitor",
                "target":entity.get("name"),
                "reason":"potential opportunity",
                "score":score
            })

    return actions
