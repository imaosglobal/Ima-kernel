"""Executable IMA social-physics contract.

Bounded research/runtime layer: not a claimed physical law.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Mapping
SOCIAL_PHYSICS_VERSION = "IMA-SOCIAL-PHYSICS-1.0"
STATUS_VALUES = ("SUPPORTED", "REJECTED", "INCONCLUSIVE", "OPEN")
@dataclass(frozen=True)
class SocialState:
    state: Mapping[str, Any] = field(default_factory=dict)
    network: Mapping[str, Any] = field(default_factory=dict)
    information: Mapping[str, Any] = field(default_factory=dict)
    environment: Mapping[str, Any] = field(default_factory=dict)
    rules_institutions: Mapping[str, Any] = field(default_factory=dict)
    history: Mapping[str, Any] = field(default_factory=dict)
    values_goals: Mapping[str, Any] = field(default_factory=dict)
    knowledge: Mapping[str, Any] = field(default_factory=dict)
    observer: Mapping[str, Any] = field(default_factory=dict)
    measurement: Mapping[str, Any] = field(default_factory=dict)
    uncertainty: Mapping[str, Any] = field(default_factory=dict)
def unified_state(state: SocialState) -> dict[str, Any]:
    return {k: dict(getattr(state, k)) for k in ("state", "network", "information", "environment", "rules_institutions", "history", "values_goals", "knowledge", "observer", "measurement", "uncertainty")}
def observed_state(state: SocialState, observation: Mapping[str, Any]) -> dict[str, Any]:
    return {"model_state": unified_state(state), "observation": dict(observation), "epistemic_status": "measurement_not_identity"}
def validate_status(status: str) -> str:
    if status not in STATUS_VALUES: raise ValueError(f"invalid epistemic status: {status}")
    return status
def intervention_gate(*, expected_benefit: float, harm: float, agency_change: float, harm_max: float = 0.0) -> dict[str, Any]:
    accepted = expected_benefit > 0 and harm <= harm_max and agency_change >= 0
    return {"accepted": accepted, "expected_benefit": expected_benefit, "harm": harm, "agency_change": agency_change, "harm_max": harm_max}
def learning_update(prior: Mapping[str, Any], *, evidence: list[Mapping[str, Any]] | None = None, contradictions: list[Mapping[str, Any]] | None = None, prediction_errors: list[Mapping[str, Any]] | None = None) -> dict[str, Any]:
    return {"prior": dict(prior), "evidence": list(evidence or []), "contradictions": list(contradictions or []), "prediction_errors": list(prediction_errors or []), "requires_reassessment": bool(contradictions or prediction_errors)}
def social_physics_contract() -> dict[str, Any]:
    return {"schema": SOCIAL_PHYSICS_VERSION, "epistemic_status": "research_framework", "formula": "D_t X_t = F(X_t,N_t,I_t,E_t,R_t,H_t,V_t,K_t) + xi_t", "required_layers": ["state", "network", "information", "environment", "rules_institutions", "history", "values_goals", "knowledge", "observer", "measurement", "uncertainty"], "network_models": ["pairwise", "higher_order", "adaptive"], "validation_statuses": list(STATUS_VALUES), "hard_constraints": ["no_analogy_as_proof", "no_correlation_as_causation", "no_simulation_as_empirical_confirmation", "privacy", "human_agency", "minimum_intervention", "explicit_uncertainty"]}
