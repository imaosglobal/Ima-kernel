
from founder.executive_ai.learning_journal.event_bus import emit_event
from founder.executive_ai.global_intelligence.opportunity_ranker import rank_opportunity



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
    # Opportunity intelligence layer
    # Keep the canonical ranking-engine schema intact
    # while enriching each opportunity with strategic signals.
    # --------------------------------------------------------
    enriched = []

    for item in ranked:
        if not isinstance(item, dict):
            continue

        opportunity = rank_opportunity(item)

        enriched_item = dict(item)
        enriched_item["opportunity_score"] = opportunity.get(
            "opportunity_score",
            item.get("rank_score", item.get("score", 0)),
        )
        enriched_item["opportunity_signals"] = opportunity.get(
            "signals",
            [],
        )

        enriched.append(enriched_item)

    ranked = enriched

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

        # Failed or unknown actions must not block future retries.
        status = (
            result.get("status")
            if isinstance(result, dict)
            else None
        )

        blocked_statuses = {
            "unknown_action",
            "execution_failed",
            "EXECUTION_FAILED",
            "CAPABILITY_MISSING",
            "CAPABILITY_NOT_CALLABLE",
            "error",
            "failed",
        }

        if status not in blocked_statuses:
            seen.add((
                str(action_name),
                str(target)
            ))

    actions = []

    for item in ranked:
        base_score = float(
            item.get("rank_score", item.get("score", 0))
        )

        opportunity_score = float(
            item.get("opportunity_score", base_score)
        )

        target = item["title"]

        # Opportunity intelligence becomes the decision signal,
        # while retaining the canonical ranking score as fallback.
        decision_score = opportunity_score

        if decision_score >= 50:
            action_name = "create_personal_outreach"
            reason = "high opportunity signal"

        elif decision_score >= 25:
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
            "score": decision_score,
            "base_score": base_score,
            "opportunity_score": opportunity_score,
            "opportunity_signals": item.get(
                "opportunity_signals",
                [],
            ),
        })

        seen.add(fingerprint)

    return actions

