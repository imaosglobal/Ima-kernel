
try:
    from founder.executive_ai.learning_journal.event_bus import emit_event
except ImportError:
    def emit_event(*args, **kwargs):
        # Optional learning-journal dependency.
        # Opportunity generation must remain operational if the journal
        # subsystem is unavailable.
        return None



from founder.executive_ai.global_intelligence.world_scanner import world_scanner
from founder.executive_ai.global_intelligence.ranking_engine import ranker
from founder.executive_ai.action_engine.action_memory import get_actions
from founder.executive_ai.economic_intelligence.economic_engine import evaluate_action_economics



def _ima_collect_opportunities():
    """Collect existing internal opportunities without external I/O."""
    found = []

    # Existing opportunity engine
    try:
        from founder.executive_ai.global_intelligence import opportunity_engine

        for name in dir(opportunity_engine):
            obj = getattr(opportunity_engine, name)

            if not callable(obj):
                continue

            lname = name.lower()

            if not any(
                x in lname
                for x in ("opportun", "discover", "signal", "prospect")
            ):
                continue

            try:
                value = obj()
            except TypeError:
                continue
            except Exception:
                continue

            if isinstance(value, dict):
                value = [value]

            if isinstance(value, (list, tuple)):
                found.extend(
                    x for x in value
                    if isinstance(x, dict)
                )
    except Exception:
        pass

    # Existing lead finder
    if not found:
        try:
            from founder.executive_ai.action_engine.executors.lead_finder import (
                find_leads,
            )

            value = find_leads({})

            if isinstance(value, dict):
                value = value.get("leads", [])

            if isinstance(value, (list, tuple)):
                found.extend(
                    x for x in value
                    if isinstance(x, dict)
                )
        except Exception:
            pass

    normalized = []
    seen = set()

    for item in found:
        target = (
            item.get("target")
            or item.get("name")
            or item.get("customer")
            or item.get("organization")
            or item.get("company")
        )

        if not target:
            continue

        score = (
            item.get("score")
            if item.get("score") is not None
            else item.get("opportunity_score", 50)
        )

        try:
            score = float(score)
        except Exception:
            score = 50.0

        key = str(target)

        if key in seen:
            continue

        seen.add(key)

        normalized.append({
            **item,
            "target": str(target),
            "score": score,
        })

    return normalized

def generate_actions():
    """
    Canonical intelligence -> executable action conversion.

    The source of truth is opportunity_engine.evaluate_world().
    No synthetic lead fallback is used here.
    """
    from founder.executive_ai.global_intelligence.opportunity_engine import (
        evaluate_world,
    )

    result = evaluate_world()

    if not isinstance(result, dict):
        raise RuntimeError(
            "Canonical intelligence returned unexpected type: "
            + type(result).__name__
        )

    opportunities = result.get("all_opportunities", [])

    if not isinstance(opportunities, list):
        raise RuntimeError(
            "Canonical intelligence returned invalid all_opportunities"
        )

    actions = []

    for item in opportunities:
        if not isinstance(item, dict):
            continue

        entity = item.get("entity") or {}

        target = (
            item.get("target")
            or entity.get("name")
            or item.get("name")
        )

        if not target:
            continue

        economics = item.get("economics") or {}

        action_name = (
            economics.get("action")
            or item.get("recommended_action")
        )

        if not action_name:
            final_score = float(item.get("final_score", 0))

            action_name = (
                "create_personal_outreach"
                if final_score >= 60
                else "monitor"
            )

        actions.append({
            "action": action_name,
            "target": str(target),
            "reason": (
                item.get("reason")
                or item.get("reasoning", {}).get("recommended_direction")
                or "canonical opportunity intelligence decision"
            ),
            "score": float(item.get("final_score", 0)),
            "opportunity_score": float(
                item.get("opportunity_score", 0)
            ),
            "economic_score": float(
                item.get("economic_score", 0)
            ),
            "signals": item.get("signals", []),
            "economics": economics,
            "reasoning": item.get("reasoning", {}),
        })

    actions.sort(
        key=lambda x: x.get("score", 0),
        reverse=True,
    )

    return actions

