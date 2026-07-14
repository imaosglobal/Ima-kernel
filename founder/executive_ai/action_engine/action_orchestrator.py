from founder.executive_ai.global_intelligence.opportunity_to_action import generate_actions
from founder.executive_ai.action_engine.action_executor import execute_action
from founder.executive_ai.action_engine.action_memory import save_action
from founder.executive_ai.global_intelligence.human_profile_engine import build_human_profile
from founder.executive_ai.action_engine.outreach_personalizer import personalize_outreach
from founder.executive_ai.action_engine.strategy_feedback_bridge import apply_feedback_to_strategy


def run_world_actions():

    actions = generate_actions()

    results=[]

    for action in actions:

        if action["action"]=="create_personal_outreach":

            profile = build_human_profile(
                {
                    "name": action["target"],
                    "country": action.get("country","unknown")
                },
                ""
            )

            result = personalize_outreach(
                profile,
                "IMA collaboration"
            )

        elif action["action"]=="monitor":

            result={
                "status":"monitoring",
                "target":action["target"]
            }

        else:
            result={
                "status":"unknown_action"
            }


        save_action(
            action["action"],
            result,
            "IMA learned from world opportunity"
        )


        results.append({
            "action":action,
            "result":result
        })


    
    strategy_update = apply_feedback_to_strategy(
        results
    )

    return {
        "actions": results,
        "strategy_update": strategy_update
    }

