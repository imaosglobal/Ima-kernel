"""Long-horizon foresight for IMA.

Foresight is treated as scenario planning, not prediction. It produces
testable trajectories and near-term actions without claiming certainty.
"""
from dataclasses import dataclass, field
from typing import Iterable

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
    confidence: str = "HYPOTHESIS"

def create_trajectory(horizon, outcome, prerequisites=(), signals=(), first_actions=(), confidence="HYPOTHESIS"):
    return FutureCapability(horizon, outcome, list(prerequisites), list(signals), list(first_actions), confidence)

def near_term_actions(trajectory: FutureCapability):
    return [{"action": action, "reason": "prepare for a possible future capability"} for action in trajectory.first_actions]

def trajectory_packet(trajectory: FutureCapability):
    return {
        "horizon": trajectory.horizon.label,
        "months": trajectory.horizon.months,
        "outcome": trajectory.outcome,
        "prerequisites": list(trajectory.prerequisites),
        "signals": list(trajectory.signals),
        "first_actions": list(trajectory.first_actions),
        "confidence": trajectory.confidence,
        "rule": "future scenario -> signals -> prerequisites -> safe present action -> re-evaluate",
    }
