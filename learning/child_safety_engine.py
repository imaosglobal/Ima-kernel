"""Deterministic first-pass safeguards for child-facing IMA experiences.

This is a risk flagger, not a complete moderation or clinical system. Integrators
must call evaluate_interaction on actual inputs/outputs and combine it with
provider safeguards, human escalation, local law, and independent testing.
"""
from __future__ import annotations

import re
from typing import Any, Dict

AGE_BANDS = {"under_5", "6_9", "10_12", "13_15", "16_17", "adult", "unknown"}

# High-precision starter signals. Expand with multilingual evaluation, not only
# keyword lists, before claiming comprehensive child-safety coverage.
_SELF_HARM = re.compile(
    r"\b(suicid(?:e|al)|kill myself|hurt myself|self[- ]harm|end my life)\b|"
    r"(להתאבד|אובדני|לפגוע בעצמי|לגמור עם החיים)",
    re.IGNORECASE,
)
_SEXUAL = re.compile(
    r"\b(sexual roleplay|send nudes|explicit sexual|erotic|sexual relationship)\b|"
    r"(תמונות עירום|יחסי מין|תוכן מיני מפורש)",
    re.IGNORECASE,
)
_SECRECY = re.compile(
    r"\b(don't tell your parents|keep this secret from your parents|only trust me)\b|"
    r"(אל תספר להורים|שמור את זה בסוד מההורים|רק תסמוך עליי)",
    re.IGNORECASE,
)
_DEPENDENCY = re.compile(
    r"\b(you only need me|i am the only one who understands you|don't talk to anyone else)\b|"
    r"(אתה צריך רק אותי|אני היחידה שמבינה אותך|אל תדבר עם אף אחד אחר)",
    re.IGNORECASE,
)
_SENSITIVE_DATA = re.compile(
    r"\b(tell me your password|send your home address|what is your exact location|"
    r"give me your school name and address)\b|"
    r"(מה הסיסמה שלך|שלח את כתובת הבית שלך|מה המיקום המדויק שלך)",
    re.IGNORECASE,
)


def evaluate_interaction(
    age_band: str = "unknown",
    user_message: str = "",
    assistant_response: str = "",
) -> Dict[str, Any]:
    """Return a conservative, explainable interaction risk assessment."""
    band = age_band if age_band in AGE_BANDS else "unknown"
    user_text = str(user_message or "")
    assistant_text = str(assistant_response or "")
    combined = user_text + "\n" + assistant_text
    minor = band != "adult"
    risks = []

    if _SELF_HARM.search(user_text):
        risks.append("possible_self_harm_disclosure")
    if minor and _SEXUAL.search(assistant_text):
        risks.append("sexual_content_in_minor_or_unknown_age_interaction")
    if minor and _SECRECY.search(assistant_text):
        risks.append("secrecy_from_caregivers")
    if minor and _DEPENDENCY.search(assistant_text):
        risks.append("emotional_dependency_or_isolation")
    if minor and _SENSITIVE_DATA.search(assistant_text):
        risks.append("sensitive_personal_data_request")

    urgent = "possible_self_harm_disclosure" in risks
    blocked = any(
        code in risks
        for code in (
            "sexual_content_in_minor_or_unknown_age_interaction",
            "secrecy_from_caregivers",
            "emotional_dependency_or_isolation",
            "sensitive_personal_data_request",
        )
    )
    if urgent:
        action = "supportive_response_and_trusted_human_or_local_crisis_support"
    elif blocked:
        action = "block_or_rewrite_response_before_delivery"
    else:
        action = "allow_subject_to_platform_safety_and_age_appropriate_review"

    return {
        "policy_version": "child-safety-first-pass-v1",
        "age_band": band,
        "protective_mode": minor,
        "allowed": not blocked,
        "risk_codes": risks,
        "recommended_action": action,
        "requires_human_review": bool(risks),
        "limitations": (
            "Keyword screening only; not comprehensive, not a clinical assessment, "
            "and not a substitute for runtime integration or independent review."
        ),
    }


def enforce_response(
    age_band: str = "unknown",
    user_message: str = "",
    assistant_response: str = "",
    language: str = "he",
) -> Dict[str, Any]:
    """Screen a candidate response and provide a safe fallback for flagged output."""
    result = evaluate_interaction(age_band, user_message, assistant_response)
    response = str(assistant_response or "")
    if "possible_self_harm_disclosure" in result["risk_codes"]:
        if str(language).lower().startswith("he"):
            response = (
                "אני מצטערת שאת/ה עובר/ת את זה. חשוב שלא תישאר/י עם זה לבד: "
                "פנה/י עכשיו לאדם שאת/ה סומך/ת עליו ובקש/י שיישאר איתך. "
                "אם יש סכנה מיידית, פנה/י לשירותי החירום המקומיים. "
                "האם את/ה בסכנה מיידית כרגע?"
            )
        else:
            response = (
                "I'm sorry you're going through this. Please don't handle it alone: "
                "contact a trusted person now and ask them to stay with you. "
                "If there is immediate danger, contact local emergency services. "
                "Are you in immediate danger right now?"
            )
        result["response_action"] = "replaced_with_supportive_safety_response"
    elif not result["allowed"]:
        if str(language).lower().startswith("he"):
            response = (
                "אני לא יכולה לעזור באופן הזה. אפשר להמשיך בדרך בטוחה שמכבדת "
                "פרטיות, גבולות וקשרים עם אנשים שאפשר לסמוך עליהם."
            )
        else:
            response = (
                "I can't help in that way. We can continue in a safer direction "
                "that respects privacy, boundaries, and trusted human relationships."
            )
        result["response_action"] = "replaced_with_safe_fallback"
    else:
        result["response_action"] = "candidate_response_passed_first_pass_screen"
    result["response"] = response
    return result


def check(interaction: Dict[str, Any] | None = None) -> bool:
    """Compatibility entry point; fail closed when no interaction is supplied."""
    if not isinstance(interaction, dict):
        return False
    result = evaluate_interaction(
        age_band=str(interaction.get("age_band", "unknown")),
        user_message=str(interaction.get("user_message", "")),
        assistant_response=str(interaction.get("assistant_response", "")),
    )
    return bool(result["allowed"] and not result["requires_human_review"])
