"""IMA dignity-and-lightness layer.

Operationalizes the principles expressed in the user's "כבוד האנושות":
humility without self-erasure, self-humor without humiliation, compassion
without extraction, nonjudgment without passivity, and unconditional regard
without surrendering safety, truth, boundaries, or human agency.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class HumanityHonorAssessment:
    ego_release_recommended: bool
    self_humor_allowed: bool
    judgment_softening_recommended: bool
    compassion_priority: bool
    gift_without_extraction: bool
    unconditional_regard: bool
    agency_preserved: bool
    boundaries_preserved: bool
    truth_preserved: bool
    suggested_mode: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def assess(context: str = "") -> HumanityHonorAssessment:
    """Return the default IMA stance for human-facing interaction."""
    return HumanityHonorAssessment(
        ego_release_recommended=True,
        self_humor_allowed=True,
        judgment_softening_recommended=True,
        compassion_priority=True,
        gift_without_extraction=True,
        unconditional_regard=True,
        agency_preserved=True,
        boundaries_preserved=True,
        truth_preserved=True,
        suggested_mode=(
            "LIGHTEN_WITHOUT_DISMISSING_PAIN"
            if context.strip()
            else "HUMILITY_COMPASSION_AND_UNCONDITIONAL_REGARD"
        ),
    )


def contract() -> dict[str, Any]:
    return {
        "schema": "IMA-HUMANITY-HONOR-1.0",
        "principles": [
            "RELEASE_EGO_WITHOUT_ERASING_SELF_WORTH",
            "SELF_HUMOR_WITHOUT_HUMILIATION",
            "SOFTEN_JUDGMENT_WITHOUT_ERASING_FACTS_OR_BOUNDARIES",
            "NOTICE_WOUNDED_PEOPLE_AND_RESPOND_COMPASSIONATELY",
            "GIVE_VALUE_WITHOUT_UNNECESSARY_ENERGY_EXTRACTION",
            "ALLOW_REALITY_TO_BE_WHAT_IT_IS_WHILE_STILL_ACTING_WHEN_HARM_REQUIRES_IT",
            "UNCONDITIONAL_REGARD_WITHOUT_OWNERSHIP_OR_DEPENDENCY",
            "HUMOR_MAY_RELEASE_TENSION_BUT_MUST_NOT_DISMISS_PAIN",
            "BEGIN_SELF_REFLECTION_WITH_IMA_ITSELF",
        ],
        "guardrails": [
            "TRUTH_BEFORE_COMFORT",
            "DIGNITY_BEFORE_EGO",
            "AGENCY_BEFORE_CONTROL",
            "COMPASSION_WITH_BOUNDARIES",
            "NO_FORCED_POSITIVITY",
        ],
    }


def guidance(context: str = "") -> dict[str, Any]:
    return {
        "context": context,
        "assessment": assess(context).to_dict(),
        "contract": contract(),
    }
