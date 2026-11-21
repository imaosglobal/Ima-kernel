"""Evidence-bounded competitive learning for IMA.

Turns observed competitor capabilities into measurable learning candidates.
It never copies proprietary implementation and never performs external actions.
"""
from dataclasses import dataclass, asdict
from typing import Iterable, List


@dataclass(frozen=True)
class CompetitiveLesson:
    competitor: str
    capability: str
    observed_advantage: str
    evidence: str
    gap: str
    adaptation: str
    user_benefit: str
    status: str = "REVIEW_REQUIRED"


def normalize_lessons(items: Iterable[CompetitiveLesson]) -> List[dict]:
    out = []
    for item in items:
        if not all([
            item.competitor.strip(), item.capability.strip(),
            item.observed_advantage.strip(), item.evidence.strip(),
            item.gap.strip(), item.adaptation.strip(), item.user_benefit.strip()
        ]):
            raise ValueError("competitive lesson fields must be non-empty")
        out.append(asdict(item))
    return out


def rank_lessons(items: Iterable[CompetitiveLesson]) -> List[dict]:
    lessons = normalize_lessons(items)
    # Durable advantage favors user value, interoperability, trust and repeatability.
    priority = {
        "persistent_context": 5,
        "universal_access": 5,
        "computer_use": 5,
        "workflow_execution": 5,
        "security_governance": 5,
        "multimodal": 4,
        "research": 4,
        "benchmarking": 4,
        "accessibility": 4,
        "ecosystem": 3,
    }
    for row in lessons:
        row["priority"] = priority.get(row["capability"], 2)
    return sorted(lessons, key=lambda x: (-x["priority"], x["competitor"], x["capability"]))
