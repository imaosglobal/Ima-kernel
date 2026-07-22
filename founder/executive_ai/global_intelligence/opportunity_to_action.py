
from founder.executive_ai.global_intelligence.world_adapters import real_world_scanner
from founder.executive_ai.global_intelligence.ranking_engine import ranker


def generate_actions():

    signals = real_world_scanner.scan()

    ranked = ranker.rank(
        signals
    )

    actions=[]


    for item in ranked:

        score = item["score"]


        if score >= 90:

            actions.append({

                "action":"create_personal_outreach",

                "target":item["title"],

                "reason":"high ranked opportunity",

                "score":score

            })


        elif score >= 75:

            actions.append({

                "action":"prepare_public_impact_message",

                "target":item["title"],

                "reason":"strategic opportunity",

                "score":score

            })


        else:

            actions.append({

                "action":"monitor",

                "target":item["title"],

                "reason":"low priority",

                "score":score

            })


    return actions



