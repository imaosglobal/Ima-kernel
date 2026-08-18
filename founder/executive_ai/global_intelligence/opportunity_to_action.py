
from founder.executive_ai.learning_journal.event_bus import emit_event



from founder.executive_ai.global_intelligence.world_scanner import world_scanner
from founder.executive_ai.global_intelligence.ranking_engine import ranker
from founder.executive_ai.action_engine.action_memory import get_actions


def generate_actions():
    """
    Generate canonical world actions.

    The generator is memory-aware:
    an identical action/target/score already recorded in action memory
    is not generated again.
    """

    emit_event(
        "action_engine",
        "action_generation_started",
        {},
        50
    )

    signals = world_scanner.scan_sources()
    ranked = ranker(signals)

    # --------------------------------------------------------
    # Load historical actions
    # --------------------------------------------------------
    try:
        history = get_actions()
    except Exception:
        history = []

    if not isinstance(history, list):
        history = []

    seen = set()

    for record in history:
        if not isinstance(record, dict):
            continue

        # memory_store wraps the actual action under "value".
        # Support both wrapped and legacy records.
        payload = record.get("value", record)

        if not isinstance(payload, dict):
            continue

        action = payload.get("action")
        result = payload.get("result", {})

        if isinstance(action, dict):
            action_name = action.get("action")
            target = action.get("target")
            score = action.get("score")
        else:
            action_name = action
            target = payload.get("target")
            score = payload.get("score")

        if isinstance(result, dict):
            target = result.get("target", target)
            score = result.get("score", score)

        # Historical action identity is action + target.
        # Score may legitimately change between cycles.
        seen.add((
            str(action_name),
            str(target)
        ))

    actions = []

    for item in ranked:
        score = item["rank_score"]
        target = item["title"]

        if score >= 90:
            action_name = "create_personal_outreach"
            reason = "high ranked opportunity"

        elif score >= 75:
            action_name = "prepare_public_impact_message"
            reason = "strategic opportunity"

        else:
            action_name = "monitor"
            reason = "low priority"

        fingerprint = (
            str(action_name),
            str(target)
        )

        # Do not regenerate an already recorded action.
        if fingerprint in seen:
            continue

        actions.append({
            "action": action_name,
            "target": target,
            "reason": reason,
            "score": score
        })

        seen.add(fingerprint)

    return actions

