"""Long-horizon foresight for IMA.

Foresight is scenario planning, not prediction. The engine converts a
plausible future into observable signals, prerequisites, safe present actions,
tests, and a re-evaluation condition. It is intentionally provider-neutral.
"""
from dataclasses import dataclass, field
from typing import Iterable, Mapping


@dataclass(frozen=True)
class Horizon:
    label: str
    months: int


HORIZONS = (
    Horizon("NOW", 0),
    Horizon("NEXT_90_DAYS", 3),
    Horizon("ONE_YEAR", 12),
    Horizon("THREE_YEARS", 36),
    Horizon("TEN_YEARS", 120),
)


@dataclass
class FutureCapability:
    horizon: Horizon
    outcome: str
    prerequisites: list[str] = field(default_factory=list)
    signals: list[str] = field(default_factory=list)
    first_actions: list[str] = field(default_factory=list)
    tests: list[str] = field(default_factory=list)
    reevaluate_when: list[str] = field(default_factory=list)
    confidence: str = "HYPOTHESIS"


def create_trajectory(
    horizon,
    outcome,
    prerequisites=(),
    signals=(),
    first_actions=(),
    tests=(),
    reevaluate_when=(),
    confidence="HYPOTHESIS",
):
    if confidence not in {"HYPOTHESIS", "SUPPORTED", "VERIFIED"}:
        raise ValueError("confidence must be HYPOTHESIS, SUPPORTED, or VERIFIED")
    if not outcome.strip():
        raise ValueError("outcome must not be empty")
    return FutureCapability(
        horizon,
        outcome,
        list(prerequisites),
        list(signals),
        list(first_actions),
        list(tests),
        list(reevaluate_when),
        confidence,
    )


def near_term_actions(trajectory: FutureCapability):
    return [
        {"action": action, "reason": "prepare for a possible future capability"}
        for action in trajectory.first_actions
    ]


def prioritize_actions(trajectories: Iterable[FutureCapability]):
    """Return present actions ordered by urgency horizon, without claiming certainty."""
    ranked = []
    for trajectory in trajectories:
        for action in trajectory.first_actions:
            ranked.append(
                {
                    "action": action,
                    "horizon": trajectory.horizon.label,
                    "months": trajectory.horizon.months,
                    "confidence": trajectory.confidence,
                }
            )
    return sorted(ranked, key=lambda item: (item["months"], item["action"]))


def re_evaluation_plan(trajectory: FutureCapability):
    """Make the next observation explicit instead of leaving foresight static."""
    return {
        "signals_to_watch": list(trajectory.signals),
        "reevaluate_when": list(trajectory.reevaluate_when),
        "next_step": "observe signals -> update prerequisites -> test present action -> revise trajectory",
    }


def trajectory_packet(trajectory: FutureCapability):
    return {
        "horizon": trajectory.horizon.label,
        "months": trajectory.horizon.months,
        "outcome": trajectory.outcome,
        "prerequisites": list(trajectory.prerequisites),
        "signals": list(trajectory.signals),
        "first_actions": list(trajectory.first_actions),
        "tests": list(trajectory.tests),
        "reevaluate_when": list(trajectory.reevaluate_when),
        "confidence": trajectory.confidence,
        "rule": "future scenario -> signals -> prerequisites -> safe present action -> test -> re-evaluate",
        "not_prediction": True,
    }


def system_foresight(scope: Iterable[str]) -> Mapping[str, list[dict]]:
    """Create a bounded planning frame for every IMA scope component."""
    result = {}
    for component in scope:
        trajectories = [
            create_trajectory(
                HORIZONS[0],
                f"make {component} observable and testable now",
                prerequisites=["runtime evidence", "clear ownership and consent boundaries"],
                signals=[f"verified runtime evidence for {component}"],
                first_actions=[f"inspect current {component} implementation and evidence"],
                tests=[f"run focused tests for {component}"],
                reevaluate_when=["new evidence", "test failure", "material product change"],
            ),
            create_trajectory(
                HORIZONS[1],
                f"make {component} reliable enough for the next 90 days",
                prerequisites=["passing regression tests", "measurable outcome"],
                signals=[f"stable test and usage evidence for {component}"],
                first_actions=[f"define one measurable acceptance criterion for {component}"],
                tests=[f"execute regression test and inspect runtime evidence"],
                reevaluate_when=["regression", "new dependency", "new user evidence"],
            ),
            create_trajectory(
                HORIZONS[2],
                f"prepare {component} for a one-year capability horizon",
                prerequisites=["portable architecture", "privacy and safety review", "provider alternatives where relevant"],
                signals=[f"repeated evidence that {component} remains useful"],
                first_actions=[f"audit portability, privacy, safety, and provider independence for {component}"],
                tests=[f"test the highest-risk dependency or assumption for {component}"],
                reevaluate_when=["technology shift", "policy change", "cost change", "user evidence"],
            ),
            create_trajectory(
                HORIZONS[3],
                f"preserve {component} across major platform and model changes",
                prerequisites=["portable data/provenance", "versioned interfaces", "fallback capability"],
                signals=[f"platform or model transition affecting {component}"],
                first_actions=[f"document migration and fallback requirements for {component}"],
                tests=[f"exercise the fallback path for {component}"],
                reevaluate_when=["platform transition", "provider loss", "architecture change"],
            ),
            create_trajectory(
                HORIZONS[4],
                f"keep {component} understandable and transferable across generations",
                prerequisites=["durable provenance", "portable knowledge", "human-readable documentation"],
                signals=[f"new generation or platform needs to reconstruct {component}"],
                first_actions=[f"check long-term preservation and reconstruction path for {component}"],
                tests=[f"perform a reconstruction/readability test for {component}"],
                reevaluate_when=["new generation", "new representation format", "loss of dependency"],
            ),
        ]
        result[component] = [trajectory_packet(t) for t in trajectories]
    return result
