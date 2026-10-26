"""Deterministic self-worth / compassion teaching guard for IMA.

This is not a diagnostic or therapeutic engine. It detects a small set of
language signals and returns teaching principles that preserve dignity,
accountability, boundaries and agency.
"""
from __future__ import annotations

import re

SELF_DIRECTED = (
    "אני שונא את עצמי", "אני שונאת את עצמי", "שונא את עצמי", "שונאת את עצמי",
    "אני לא שווה", "אני חסר ערך", "אני חסרת ערך", "hate myself",
    "worthless", "no one loves me", "i am nothing",
)
SHAME = (
    "בושה", "מביישים", "מושפל", "השפלה", "shame", "humiliated", "humiliation",
)
GROUP_DEHUMANIZATION = (
    "הם כולם מפלצות", "הם חיות", "תתי אדם", "they are all monsters",
    "they are animals", "subhuman",
)

def _hits(text: str, terms: tuple[str, ...]) -> list[str]:
    low = text.lower()
    return [t for t in terms if t.lower() in low]

def assess_self_worth(text: str) -> dict:
    if not isinstance(text, str) or not text.strip():
        raise ValueError("text is required")
    self_harm = _hits(text, SELF_DIRECTED)
    shame = _hits(text, SHAME)
    dehuman = _hits(text, GROUP_DEHUMANIZATION)
    risk_score = len(self_harm) * 2 + len(shame) + len(dehuman) * 3
    risk = "HIGH" if risk_score >= 4 else "MEDIUM" if risk_score >= 2 else "LOW"
    principles = [
        "DIGNITY_IS_NOT_EARNED_BY_PERFECTION",
        "FEELING_IS_NOT_ACTION",
        "MISTAKE_IS_NOT_IDENTITY",
        "ACCOUNTABILITY_WITHOUT_HUMILIATION",
        "CARE_WITHOUT_OWNERSHIP",
        "SUPPORT_WITHOUT_DEPENDENCY",
        "PERSON_IS_NOT_A_GROUP",
        "EVIDENCE_BEFORE_CAUSAL_CLAIM",
        "AGENCY_PRESERVED",
    ]
    return {
        "risk_level": risk,
        "self_directed_harm_language": bool(self_harm),
        "shame_language": bool(shame),
        "group_dehumanization": bool(dehuman),
        "signals": self_harm + shame + dehuman,
        "diagnosis": "NOT_DIAGNOSED",
        "agency_preserved": True,
        "principles": principles,
        "suggested_next_step": (
            "SAFETY_AND_TRUSTED_HUMAN_SUPPORT"
            if risk == "HIGH"
            else "NOTICE_NAME_CARE_CHECK_CHOOSE_REPAIR"
        ),
    }
