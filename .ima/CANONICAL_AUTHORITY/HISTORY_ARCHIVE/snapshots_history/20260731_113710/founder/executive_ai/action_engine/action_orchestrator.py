
from founder.executive_ai.global_intelligence.opportunity_to_action import generate_actions
from founder.executive_ai.action_engine.action_memory import save_action
from founder.executive_ai.action_engine.action_feedback_learning import learn_from_action


def run_world_actions():

    actions = generate_actions()
    results = []

    for action in actions:

        if action["action"] == "create_personal_outreach":

            result = {
                "status": "outreach_ready",
                "target": action["target"],
                "reason": action.get("reason"),
                "score": action.get("score"),
                "signals": action.get("signals", [])
            }

        elif action["action"] == "monitor":

            result = {
                "status": "monitoring",
                "target": action["target"],
                "score": action.get("score")
            }

        elif action["action"] == "prepare_public_impact_message":

            result = prepare_public_impact_message(action)

        else:

            result = {
                "status": "unknown_action",
                "action": action["action"]
            }


        save_action(
            action["action"],
            result,
            "IMA executed opportunity intelligence cycle"
        )

        learn_from_action({"action": action, "result": result})

        results.append({
            "action": action,
            "result": result
        })


    return {
        "executed": len(results),
        "results": results
    }


def prepare_public_impact_message(action):

    return {
        "status":"message_ready",
        "target":action.get("target"),
        "strategy":"public impact focused outreach"
    }

