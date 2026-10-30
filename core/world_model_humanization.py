"""Human-centered policy for interactive AI world models.

World models are simulations, not reality. This module keeps their use bounded by
evidence, provenance, consent, reversibility, accessibility and human agency.
""" 
from __future__ import annotations

POLICY_VERSION = "world-model-humanization-v1.0"

WORLD_MODEL_POLICY = {
    "simulation_is_not_reality": True,
    "require_provenance": True,
    "require_human_agency": True,
    "require_bounded_use": True,
    "require_reversible_actions": True,
    "private_data_default": "do_not_import",
    "high_impact_rule": "simulation_evidence_never_replaces_real_world_validation",
    "public_media_rule": "label_synthetic_or_simulated_media_and_preserve_origin",
    "child_rule": "child-facing simulations use age-appropriate safeguards and never normalize unsafe real-world experimentation",
    "accessibility_rule": "provide text/audio/visual alternatives where feasible",
    "uncertainty_rule": "separate measured behavior from generated plausibility",
}

def world_model_context() -> str:
    return """WORLD-MODEL HUMANIZATION
- Interactive world models can simulate environments, agents, sound and physical behavior, but a generated world is not the physical world.
- Use simulations to explore, teach, prototype and test bounded hypotheses; never present simulated outcomes as proof of real-world safety or truth.
- Preserve provenance: distinguish source observations, model-generated content, edits, assumptions and unknowns.
- Keep people in control. No simulation should silently authorize a consequential real-world action, transfer private data, or create dependence on an opaque system.
- For robotics, medicine, safety, public policy or other high-impact use, require real-world validation and appropriate human oversight in addition to simulation evidence.
- Synthetic or simulated media should be identifiable as such when that distinction matters.
- Prefer reversible, low-risk experiments; record limitations and failure modes.
- For children, favor learning and safe exploration over realistic encouragement of dangerous real-world behavior.
- When a capability is unavailable, say so; do not imply that IMA can itself generate or enter a world model unless a verified integration exists.
"""

def assess_world_model_use(context: str) -> dict[str, object]:
    text = str(context or "").strip().lower()
    high_impact = any(term in text for term in (
        "medical", "medicine", "robot", "autonomous", "driving", "safety",
        "weapon", "public policy", "critical infrastructure"
    ))
    return {
        "policy_version": POLICY_VERSION,
        "simulation_not_reality": True,
        "high_impact": high_impact,
        "real_world_validation_required": high_impact,
        "human_override_required": high_impact,
        "status": "SAFE_BOUNDED" if not high_impact else "REQUIRES_REAL_WORLD_VALIDATION",
    }
