"""IMA deterministic peace/de-escalation layer.

This module is intentionally model-agnostic: it does not decide guilt or truth.
It identifies linguistic risk signals, separates group identity from claims,
and produces a non-coercive reframe suitable for a later runtime adapter.
"""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Any

GROUP_WORDS = (
    "יהודים", "ישראלים", "איראנים", "ערבים", "מוסלמים", "נוצרים",
    "ימין", "שמאל", "דתיים", "חילונים", "גברים", "נשים", "מהגרים",
    "jews", "israelis", "iranians", "arabs", "muslims", "christians",
    "men", "women", "immigrants",
)
HARM_TERMS = (
    "להרוג", "רצח", "להשמיד", "לשרוף", "לגרש", "אונס", "תקוף", "פצצה",
    "kill", "murder", "destroy", "burn", "expel", "rape", "attack", "bomb",
)
GENERALIZERS = (
    "כולם", "אף אחד", "כל ה", "הם כאלה", "הם שונאים", "הם רוצים למות",
    "everybody", "everyone", "all ", "none ", "they all", "they hate",
)
HUMILIATION = (
    "זבל", "חיות", "מפלצות", "תתי אדם", "בהמות",
    "trash", "animals", "monsters", "subhuman",
)

@dataclass(frozen=True)
class PeaceAssessment:
    risk_level: str
    harm_signals: list[str]
    generalization_signals: list[str]
    dehumanization_signals: list[str]
    identity_generalization: bool
    needs_human_safety_review: bool
    evidence_status: str
    agency_preserved: bool
    suggested_next_step: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

def _hits(text: str, terms: tuple[str, ...]) -> list[str]:
    lower = text.lower()
    return [term for term in terms if term.lower() in lower]

def assess(text: str) -> PeaceAssessment:
    if not isinstance(text, str) or not text.strip():
        raise ValueError("text is required")
    harm = _hits(text, HARM_TERMS)
    general = _hits(text, GENERALIZERS)
    dehuman = _hits(text, HUMILIATION)
    groups = _hits(text, GROUP_WORDS)
    identity_generalization = bool(groups and general)
    score = len(harm) * 3 + len(dehuman) * 3 + len(general) * 2
    if score >= 6:
        risk = "HIGH"
    elif score >= 2:
        risk = "MEDIUM"
    else:
        risk = "LOW"
    return PeaceAssessment(
        risk_level=risk,
        harm_signals=harm,
        generalization_signals=general,
        dehumanization_signals=dehuman,
        identity_generalization=identity_generalization,
        needs_human_safety_review=bool(harm or dehuman),
        evidence_status="UNVERIFIED_CLAIM" if identity_generalization else "NO_FACT_CLAIM_VERIFICATION_PERFORMED",
        agency_preserved=True,
        suggested_next_step=(
            "STOP_HARM_AND_SEPARATE_CLAIM_FROM_GROUP_IDENTITY"
            if risk == "HIGH"
            else "CLARIFY_FACTS_CONTEXT_BOUNDARIES_AND_NONVIOLENT_OPTIONS"
        ),
    )

def reframe(text: str) -> dict[str, Any]:
    """Return a safe communication frame; never silently changes the user's claim."""
    a = assess(text)
    prefix = ""
    if a.identity_generalization:
        prefix = (
            "נסח את הטענה על פעולה, אדם או גורם מסוים במקום לייחס כוונה או אופי "
            "לקבוצה שלמה. הפרד בין מה שידוע, מה שמוערך ומה שאינו ידוע. "
        )
    elif a.needs_human_safety_review:
        prefix = (
            "יש כאן סימן אפשרי לפגיעה או הסלמה. התמקד בהגנה על אנשים, "
            "התרחקות מהסלמה ובערוצים אנושיים מוסמכים; אל תניח אשמה ללא ראיות. "
        )
    else:
        prefix = "שמור על מחלוקת עניינית: טענה, ראיות, אי-ודאות, גבולות ואפשרויות לא-אלימות. "
    return {
        "original": text,
        "assessment": a.to_dict(),
        "reframe_guidance": prefix,
        "principles": [
            "PERSON_IS_NOT_A_GROUP",
            "DETECTION_IS_NOT_GUILT",
            "EVIDENCE_BEFORE_CLAIM",
            "PROTECT_DIGNITY_AND_AGENCY",
            "NO_AUTONOMOUS_EXTERNAL_ACTION",
        ],
    }
