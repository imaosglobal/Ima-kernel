"""IMA Personal Trait & Growth Model.

Privacy-first framework for turning repeated user observations into a structured
trait model without confusing traits with thoughts, emotions, pain, beliefs,
habits, or survival responses.

User-specific records must be stored in the private runtime memory store.
Never hard-code a person's sensitive history into the public repository.
"""
from __future__ import annotations

from copy import deepcopy

SCHEMA = "IMA-PERSONAL-TRAIT-MODEL-1.0"

TRAIT_FIELDS = (
    "trait",
    "evidence",
    "strength",
    "risk_when_overactivated",
    "counter_strategy",
    "confidence",
    "last_verified",
)

CORE_LAYERS = (
    "thought",
    "emotion",
    "pain",
    "belief",
    "habit",
    "trait",
    "value",
    "identity",
)

DEFAULT_COUNTER_STRATEGIES = {
    "overactivation": (
        "pause before acting",
        "separate fact from interpretation",
        "name the current need",
        "choose the smallest useful action",
        "restore agency rather than dependency",
    ),
    "justice": (
        "distinguish injustice from ordinary disagreement",
        "define the concrete outcome sought",
        "choose proportionate action",
        "stop when the useful action is complete",
    ),
    "protectiveness": (
        "check whether danger is present now",
        "protect without permanent vigilance",
        "share responsibility when appropriate",
    ),
    "independence": (
        "ask whether help increases or decreases agency",
        "accept useful assistance without surrendering choice",
    ),
    "persistence": (
        "measure progress by evidence, not effort alone",
        "schedule recovery and stopping points",
    ),
    "sensitivity": (
        "separate signal from threat interpretation",
        "delay conclusions when emotionally activated",
    ),
    "creativity": (
        "capture ideas, then select one executable next step",
        "finish before expanding scope",
    ),
    "systems_thinking": (
        "zoom between system and smallest actionable unit",
        "verify dependencies before adding complexity",
    ),
}


def classify_layer(item: dict) -> str:
    """Return the conceptual layer of an observation."""
    layer = str(item.get("layer", "")).strip().lower()
    return layer if layer in CORE_LAYERS else "belief"


def normalize_trait(trait: dict) -> dict:
    """Normalize a trait observation without inventing evidence."""
    if not isinstance(trait, dict):
        raise ValueError("trait must be an object")
    name = str(trait.get("trait", "")).strip()
    if not name:
        raise ValueError("trait name is required")
    result = {
        "trait": name,
        "evidence": deepcopy(trait.get("evidence", [])),
        "strength": str(trait.get("strength", "")).strip(),
        "risk_when_overactivated": str(
            trait.get("risk_when_overactivated", "")
        ).strip(),
        "counter_strategy": deepcopy(
            trait.get("counter_strategy", [])
        ),
        "confidence": trait.get("confidence"),
        "last_verified": trait.get("last_verified"),
    }
    if not result["counter_strategy"]:
        key = name.lower().replace("-", "_").replace(" ", "_")
        result["counter_strategy"] = list(
            DEFAULT_COUNTER_STRATEGIES.get(key, DEFAULT_COUNTER_STRATEGIES["overactivation"])
        )
    return result


def build_profile(observations: list[dict], *, version: str = "1.0") -> dict:
    """Build an auditable profile from observations.

    The function preserves uncertainty: it does not turn one observation into
    an identity claim and does not infer a trait without evidence.
    """
    normalized = [normalize_trait(item) for item in observations]
    return {
        "schema": SCHEMA,
        "version": version,
        "layers": list(CORE_LAYERS),
        "traits": normalized,
        "rules": {
            "pain_is_not_identity": True,
            "belief_is_not_fact": True,
            "survival_response_is_not_character": True,
            "trait_is_not_destiny": True,
            "identity_remains_user_owned": True,
            "agency_over_dependency": True,
        },
    }


def growth_prompt(profile: dict) -> str:
    """Return the runtime instruction used when helping a user study traits."""
    return (
        "Help the user distinguish thoughts, emotions, pain, beliefs, habits, "
        "traits, values and identity. Treat trait hypotheses as revisable. "
        "For every trait, surface both its useful function and its "
        "overactivation risk, then offer a concrete counter-strategy. "
        "Do not define the user by trauma, pain, diagnosis, conflict or any "
        "single period of life. Prefer evidence from repeated behavior and "
        "the user's own corrections. Preserve agency: IMA may illuminate "
        "patterns, but the person decides who they are and what to change."
    )
