"""Provider-neutral routing policy for IMA's distributed knowledge mesh."""

from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Iterable, Mapping

TRUTH_STATES = {"observed", "reported", "inferred", "verified", "disputed", "unknown", "retired"}

@dataclass(frozen=True)
class SourceObservation:
    source_id: str
    source_type: str
    domain: str
    modality: str
    observed_at: str
    truth_state: str
    provenance: Mapping[str, object]
    authorized: bool = False

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.source_id: errors.append("source_id_required")
        if self.truth_state not in TRUTH_STATES: errors.append("invalid_truth_state")
        if not self.provenance: errors.append("provenance_required")
        if not self.authorized: errors.append("source_not_authorized")
        return errors

@dataclass(frozen=True)
class LearningPlan:
    source_id: str
    stages: tuple[str, ...]
    safe_to_integrate: bool
    reason: str
    def as_dict(self) -> dict[str, object]:
        return asdict(self)

def plan_learning(observation: SourceObservation) -> LearningPlan:
    errors = observation.validate()
    if errors:
        return LearningPlan(observation.source_id, ("reject",), False, ",".join(errors))
    stages = ("classify", "cross_check", "extract_capability", "benchmark",
              "integrate_derived_knowledge", "record_provenance", "reassess")
    safe = observation.truth_state in {"observed", "verified"} and observation.authorized
    reason = "authorized_verified_or_observed_source" if safe else "requires_additional_verification"
    return LearningPlan(observation.source_id, stages, safe, reason)

def batch_plan(observations: Iterable[SourceObservation]) -> list[dict[str, object]]:
    return [plan_learning(item).as_dict() for item in observations]
