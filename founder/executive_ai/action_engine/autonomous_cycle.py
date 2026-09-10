from founder.executive_ai.action_engine.action_orchestrator import run_world_actions
from founder.executive_ai.action_engine.action_learning_loop import learning_cycle
from learning.self_improvement import run_self_improvement


def run_cycle():
    """
    IMA canonical autonomous cycle.

    Diagnose -> Observe -> Decide -> Act -> Learn.
    """

    print("=== IMA AUTONOMOUS CYCLE START ===")

    print("[DIAGNOSE]")
    from learning.self_improvement import run_self_improvement
    self_development = run_self_improvement()

    print("[OBSERVE]")
    from founder.executive_ai.global_intelligence.world_scanner import world_scanner
    discoveries = world_scanner.scan_sources() or []

    print("[DECIDE]")
    from learning.decision_engine import make_learning_decision

    opportunities = []

    for discovery in discoveries:
        if not isinstance(discovery, dict):
            continue

        area = (
            discovery.get("category")
            or discovery.get("source")
            or "world_discovery"
        )

        reason = (
            discovery.get("title")
            or discovery.get("content")
            or "new discovery"
        )

        decision = make_learning_decision(
            area=str(area),
            reason=str(reason),
        )

        if decision is not None:
            opportunity = dict(discovery)
            opportunity["decision"] = decision
            opportunity["decision_area"] = str(area)
            opportunity["decision_reason"] = str(reason)
            if "opportunity_score" not in opportunity:
                opportunity["opportunity_score"] = float(
                    opportunity.get(
                        "importance",
                        opportunity.get(
                            "rank_score",
                            opportunity.get("score", 0),
                        ),
                    ) or 0
                )
            opportunities.append(opportunity)

    print("[ACT]")
    from founder.executive_ai.action_engine.action_orchestrator import run_world_actions
    actions = run_world_actions(opportunities=opportunities) or []

    print("[LEARN]")
    from learning.learning_loop import learn_from_event

    learning_event = {
        "event_type": "autonomous_cycle",
        "source": "IMA",
        "text": (
            f"IMA autonomous cycle completed: "
            f"{len(discoveries)} discoveries, "
            f"{len(opportunities)} opportunities, "
            f"{len(actions)} actions"
        ),
        "topic": "autonomous_cycle",
        "discoveries": discoveries,
        "opportunities": opportunities,
        "actions": actions,
        "self_development": self_development,
    }

    learning = learn_from_event(learning_event)

    result = {
        "self_development": self_development,
        "discoveries": discoveries,
        "opportunities": opportunities,
        "actions": actions,
        "learning": learning,
        "status": "cycle_completed",
    }

    print("=== IMA AUTONOMOUS CYCLE COMPLETE ===")
    return result


if __name__ == "__main__":
    result = run_cycle()
    print(result)
