
from founder.executive_ai.global_intelligence.opportunity_to_action import generate_actions
from founder.executive_ai.action_engine.action_memory import save_action
from founder.executive_ai.action_engine.action_feedback_learning import learn_from_action


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
        record = {
            "action": action,
            **result,
        }

        try:
            save_action(record)
        except Exception as exc:
            record["save_error"] = str(exc)

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

