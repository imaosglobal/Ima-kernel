"""Normalize lessons from similar and dissimilar products without copying product identity.

Patterns are evidence, not authorities. The output is a reviewable lesson ledger.
"""

from dataclasses import dataclass, asdict
from typing import Iterable


@dataclass(frozen=True)
class EcosystemLesson:
    source: str
    domain: str
    lesson: str
    overlap: str
    adaptation: str
    status: str = "REVIEW_REQUIRED"


def normalize_lessons(items: Iterable[dict]) -> list[dict]:
    out = []
    for item in items:
        required = ("source", "domain", "lesson", "overlap", "adaptation")
        if not all(str(item.get(k, "")).strip() for k in required):
            continue
        out.append(asdict(EcosystemLesson(
            source=str(item["source"]).strip(),
            domain=str(item["domain"]).strip(),
            lesson=str(item["lesson"]).strip(),
            overlap=str(item["overlap"]).strip(),
            adaptation=str(item["adaptation"]).strip(),
        )))
    return out
