"""Evidence-bounded self-improvement signals migrated from IMA evolving-home.

This module observes supplied metrics/feedback and produces improvement candidates.
It never self-modifies code, deploys, changes user state, or executes external actions.
"""
from dataclasses import dataclass
from typing import Iterable, Mapping


@dataclass(frozen=True)
class ImprovementCandidate:
    area: str
    reason: str
    evidence: str
    priority: str


def derive_candidates(
    metrics: Mapping[str, float],
    feedback: Iterable[Mapping[str, object]] = (),
) -> list[ImprovementCandidate]:
    candidates: list[ImprovementCandidate] = []

    if metrics.get("error_rate", 0.0) > 0.05:
        candidates.append(
            ImprovementCandidate(
                "reliability",
                "Observed error rate exceeds 5%.",
                f"error_rate={metrics['error_rate']}",
                "high",
            )
        )

    if metrics.get("task_success_rate", 1.0) < 0.8:
        candidates.append(
            ImprovementCandidate(
                "task_success",
                "Observed task success rate is below 80%.",
                f"task_success_rate={metrics['task_success_rate']}",
                "high",
            )
        )

    negative = sum(1 for item in feedback if item.get("sentiment") == "negative")
    if negative:
        candidates.append(
            ImprovementCandidate(
                "user_feedback",
                "Negative feedback was observed.",
                f"negative_feedback_count={negative}",
                "medium",
            )
        )

    return candidates
