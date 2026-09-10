
from founder.executive_ai.learning_journal.event_bus import emit_event
from founder.executive_ai.global_intelligence.opportunity_ranker import rank_opportunity



from founder.executive_ai.global_intelligence.world_scanner import world_scanner
from founder.executive_ai.global_intelligence.ranking_engine import ranker
from founder.executive_ai.action_engine.action_memory import get_actions


def generate_actions(opportunities=None):
    """
    Canonical Opportunity -> Action bridge.

    If opportunities are supplied, they are reused directly.
    Otherwise the function performs the legacy observe/rank path.
    """
    emit_event(
        "action_engine",
        "opportunity_action_generation_started",
        {},
        50,
    )

    actions = []
    seen = set()

    try:
        # Reuse already-observed opportunities whenever available.
        if opportunities is None:
            discoveries = world_scanner.scan_sources()
            ranked = ranker(discoveries) if isinstance(discoveries, list) else []

            opportunities = []

            for item in ranked:
                if not isinstance(item, dict):
                    continue

                try:
                    opportunity = rank_opportunity(item)
                except Exception:
                    continue

                if not isinstance(opportunity, dict):
                    continue

                enriched = dict(item)
                enriched["opportunity_score"] = opportunity.get(
                    "opportunity_score",
                    item.get("rank_score", item.get("score", 0)),
                )
                enriched["opportunity_signals"] = opportunity.get(
                    "signals",
                    [],
                )
                opportunities.append(enriched)

        if not isinstance(opportunities, list):
            opportunities = []

        for item in opportunities:
            if not isinstance(item, dict):
                continue

            score = float(
                item.get(
                    "opportunity_score",
                    item.get("rank_score", item.get("score", 0)),
                ) or 0
            )

            if score < 20:
                continue

            target = str(
                item.get("title")
                or item.get("name")
                or "world discovery"
            ).strip()

            if score >= 50:
                action_name = "create_personal_outreach"
                reason = "high opportunity signal"
            elif score >= 25:
                action_name = "prepare_public_impact_message"
                reason = "strategic opportunity"
            else:
                action_name = "monitor"
                reason = "relevant world discovery"

            fingerprint = (action_name, target.casefold())

            if fingerprint in seen:
                continue

            seen.add(fingerprint)

            actions.append({
                "action": action_name,
                "target": target,
                "reason": reason,
                "score": score,
                "base_score": float(
                    item.get("rank_score", item.get("score", 0)) or 0
                ),
                "opportunity_score": score,
                "opportunity_signals": item.get(
                    "opportunity_signals",
                    item.get("signals", []),
                ),
                "source": item.get("source", ""),
                "content": str(item.get("content", ""))[:5000],
                "url": item.get("url", ""),
            })

    except Exception as exc:
        emit_event(
            "action_engine",
            "opportunity_action_generation_failed",
            {"error": repr(exc)},
            100,
        )
        return []

    emit_event(
        "action_engine",
        "opportunity_action_generation_completed",
        {"actions": len(actions)},
        50,
    )

    return actions

