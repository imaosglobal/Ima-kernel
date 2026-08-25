
from founder.executive_ai.global_intelligence.opportunity_to_action import generate_actions
from founder.executive_ai.action_engine.action_memory import save_action
from founder.executive_ai.action_engine.action_feedback_learning import learn_from_action
from founder.executive_ai.economic_intelligence.economic_engine import evaluate_action_economics
from founder.executive_ai.action_engine.action_orchestrator_patch import dispatch_new_actions



def run_world_actions():
    """
    Canonical world-action dispatcher.

    Responsibilities:
    - normalize nested/legacy action records
    - dispatch known actions
    - never silently convert a known action into unknown_action
    - deduplicate identical actions within one cycle
    """

    actions = generate_actions()
    results = []
    seen = set()

    for raw_action in actions:
        if not isinstance(raw_action, dict):
            continue

        # --------------------------------------------------------
        # Normalize nested action records
        # --------------------------------------------------------
        nested = raw_action.get("action")

        if isinstance(nested, dict):
            action_name = nested.get("action")
            action = dict(raw_action)

            if nested.get("target") is not None:
                action["target"] = nested["target"]

            if nested.get("score") is not None:
                action["score"] = nested["score"]

            action["action"] = action_name
        else:
            action = dict(raw_action)
            action_name = nested

        target = action.get("target")
        score = action.get("score")

        # Economic decision layer
        try:
            economics = action.get("economics")
            if not isinstance(economics, dict):
                economics = evaluate_action_economics(action)
        except Exception as exc:
            economics = {
                "status": "economic_evaluation_error",
                "error": str(exc),
            }

        economic_score = action.get(
            "economic_score",
            economics.get("economic_score", 0)
            if isinstance(economics, dict) else 0
        )

        action["economics"] = economics
        action["economic_score"] = economic_score


        # --------------------------------------------------------
        # Prevent duplicate execution inside one autonomous cycle
        # --------------------------------------------------------
        fingerprint = (
            str(action_name),
            str(target),
            str(score),
        )

        if fingerprint in seen:
            continue

        seen.add(fingerprint)

        # --------------------------------------------------------
        # Canonical dispatch
        # --------------------------------------------------------
        if action_name == "create_personal_outreach":
            result = {
                "status": "outreach_ready",
                "target": target,
                "score": score,
            }


        # --------------------------------------------------------
        # NEW: Treasury + Impact + Education dispatch
        # --------------------------------------------------------
        treasury_result = dispatch_new_actions(action_name, action)
        if treasury_result is not None:
            result = treasury_result
        elif action_name == "prepare_public_impact_message":
            result = prepare_public_impact_message(action)

        elif action_name == "monitor":
            result = {
                "status": "monitoring",
                "target": target,
                "score": score,
            }

        else:
            result = {
                "status": "unknown_action",
                "target": target,
                "score": score,
                "action": action_name,
            }

        # --------------------------------------------------------
        # Persist action + feed the learning layer
        # --------------------------------------------------------
        try:
            economics = evaluate_action_economics(action)
        except Exception as exc:
            economics = {
                "status": "economic_evaluation_error",
                "error": str(exc),
            }

        record = {
"action": action,
            **result,
            "economics": economics,
            "economic_score": economic_score,
        }

        try:
            save_action(action, result, result.get("reason", result.get("status", "action execution")))
        except Exception as exc:
            record["save_error"] = str(exc)

        # --------------------------------------------------------
        # Economic outcome bridge
        # --------------------------------------------------------
        # Economic outcomes are only recorded when an actual
        # observable outcome exists. Planning/execution alone
        # must never be treated as revenue.
        #
        # Import locally to keep the action-learning graph acyclic.
        # --------------------------------------------------------
        if isinstance(result, dict) and result.get("actual_outcome"):
            try:
                from founder.executive_ai.economic_intelligence.economic_feedback_bridge import (
                    process_economic_outcome,
                )

                economic_outcome = result["actual_outcome"]

                economic_cycle = process_economic_outcome(
                    action,
                    economic_outcome,
                )

                result["economic_feedback"] = economic_cycle

            except Exception as exc:
                result["economic_feedback_error"] = str(exc)

        try:
            learn_from_action(action, result)
        except Exception as exc:
            record["learning_error"] = str(exc)

        # --------------------------------------------------------
        # Canonical result envelope
        # --------------------------------------------------------
        results.append(record)

    return results

def prepare_public_impact_message(action):

    return {
        "status":"message_ready",
        "target":action.get("target"),
        "strategy":"public impact focused outreach"
    }

