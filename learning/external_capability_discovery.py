"""Daily external capability discovery contract.

This module normalizes externally discovered candidates into a reviewable ledger.
It never installs dependencies, copies secrets, executes external code, or promotes
a candidate to a live capability.
"""

from dataclasses import dataclass, asdict
from typing import Iterable


@dataclass(frozen=True)
class CapabilityCandidate:
    source: str
    name: str
    evidence_url: str
    capability: str
    conflict_status: str = "REVIEW_REQUIRED"


def normalize_candidates(items: Iterable[dict]) -> list[dict]:
    out = []
    for item in items:
        required = ("source", "name", "evidence_url", "capability")
        if not all(str(item.get(k, "")).strip() for k in required):
            continue
        candidate = CapabilityCandidate(
            source=str(item["source"]).strip(),
            name=str(item["name"]).strip(),
            evidence_url=str(item["evidence_url"]).strip(),
            capability=str(item["capability"]).strip(),
        )
        out.append(asdict(candidate))
    return out
