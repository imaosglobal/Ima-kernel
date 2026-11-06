"""IMA Global Change & Humanitarian Intelligence.

Provider-neutral, evidence-first primitives for recognizing major human/world
changes and mapping safe, nonviolent, humanitarian responses.

This module does not decide who is right, assign guilt, contact authorities,
send aid, or execute external actions. It normalizes observations so higher
layers can verify them, compare historical outcomes, identify needs, and
present authorized options while preserving human agency.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

EVENT_TYPES = (
    "CONFLICT", "PROTEST_OR_UPRISING", "POLITICAL_CHANGE", "DISASTER",
    "PUBLIC_HEALTH", "HUMANITARIAN_DISPLACEMENT", "RESOURCE_CRISIS",
    "TECHNOLOGICAL_SHIFT", "SCIENTIFIC_SHIFT", "CULTURAL_OR_SOCIAL_SHIFT", "UNKNOWN",
)

NEEDS_BY_TYPE = {
    "CONFLICT": ("safety", "verified_information", "medical_care", "water_food_shelter",
                 "family_reconnection", "displacement_support", "de_escalation"),
    "PROTEST_OR_UPRISING": ("safety", "verified_information", "freedom_of_expression",
                            "nonviolent_dialogue", "medical_support", "legal_information"),
    "POLITICAL_CHANGE": ("verified_information", "translation", "civic_access",
                         "institutional_continuity", "peaceful_dialogue"),
    "DISASTER": ("rescue", "medical_care", "water_food_shelter", "power",
                 "communications", "family_reconnection", "recovery"),
    "PUBLIC_HEALTH": ("medical_care", "verified_information", "prevention",
                      "accessibility", "continuity_of_care"),
    "HUMANITARIAN_DISPLACEMENT": ("safe_shelter", "food_water", "medical_care",
                                  "documentation", "family_reconnection", "legal_information"),
    "RESOURCE_CRISIS": ("water_food_energy", "verified_information", "fair_distribution",
                        "local_capacity", "peaceful_coordination"),
    "TECHNOLOGICAL_SHIFT": ("public_understanding", "safety_review", "education",
                            "accessibility", "workforce_adaptation"),
    "SCIENTIFIC_SHIFT": ("public_understanding", "evidence_review", "education",
                         "responsible_translation"),
    "CULTURAL_OR_SOCIAL_SHIFT": ("listening", "translation", "pluralism",
                                 "dialogue", "community_support"),
    "UNKNOWN": ("verified_information", "context", "human_review"),
}

NONVIOLENT_ACTIONS = (
    "LISTEN_TO_LOCAL_PEOPLE", "VERIFY_MULTIPLE_INDEPENDENT_SOURCES",
    "SEPARATE_FACTS_FROM_CLAIMS", "TRANSLATE_AND_CLARIFY", "MAP_IMMEDIATE_NEEDS",
    "CONNECT_TO_AUTHORIZED_HELP", "SUPPORT_NONVIOLENT_DIALOGUE",
    "DOCUMENT_OUTCOMES", "REASSESS",
)

@dataclass(frozen=True)
class WorldObservation:
    title: str
    event_type: str
    place: str | None
    observed_at: str
    source_url: str
    source_name: str
    evidence_status: str = "UNVERIFIED"
    confidence: str = "UNKNOWN"
    affected_groups: tuple[str, ...] = ()
    summary: str = ""
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

@dataclass(frozen=True)
class HumanitarianPlan:
    event_type: str
    needs: tuple[str, ...]
    nonviolent_actions: tuple[str, ...]
    agency_rule: str
    safety_rule: str
    verification_rule: str
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

def classify_text(text: str) -> str:
    value = str(text or "").casefold()
    if any(x in value for x in ("earthquake", "flood", "wildfire", "hurricane", "cyclone",
                                "tsunami", "רעידת אדמה", "שיטפון", "שריפה", "הצפה")):
        return "DISASTER"
    if any(x in value for x in ("war", "armed conflict", "airstrike", "bombing",
                                "מלחמה", "לחימה", "תקיפה", "הפצצה", "סכסוך")):
        return "CONFLICT"
    if any(x in value for x in ("protest", "uprising", "demonstration", "strike",
                                "מחאה", "מרד", "הפגנה", "שביתה")):
        return "PROTEST_OR_UPRISING"
    if any(x in value for x in ("election", "coup", "government", "president", "elections",
                                "בחירות", "הפיכה", "ממשלה", "נשיא")):
        return "POLITICAL_CHANGE"
    if any(x in value for x in ("outbreak", "epidemic", "pandemic", "cholera", "health emergency",
                                "מגפה", "התפרצות", "בריאות")):
        return "PUBLIC_HEALTH"
    if any(x in value for x in ("refugee", "displaced", "displacement", "פליטים", "עקורים")):
        return "HUMANITARIAN_DISPLACEMENT"
    if any(x in value for x in ("famine", "food shortage", "water shortage", "energy crisis",
                                "רעב", "מחסור במים", "משבר אנרגיה")):
        return "RESOURCE_CRISIS"
    if any(x in value for x in ("breakthrough", "new technology", "ai model", "technology",
                                "פריצת דרך", "טכנולוגיה", "בינה מלאכותית")):
        return "TECHNOLOGICAL_SHIFT"
    if any(x in value for x in ("research", "scientific", "discovery", "מחקר", "גילוי מדעי")):
        return "SCIENTIFIC_SHIFT"
    if any(x in value for x in ("culture", "social movement", "society", "תרבות", "תנועה חברתית")):
        return "CULTURAL_OR_SOCIAL_SHIFT"
    return "UNKNOWN"

def build_humanitarian_plan(event_type: str) -> HumanitarianPlan:
    kind = event_type if event_type in EVENT_TYPES else "UNKNOWN"
    return HumanitarianPlan(
        event_type=kind,
        needs=tuple(NEEDS_BY_TYPE[kind]),
        nonviolent_actions=NONVIOLENT_ACTIONS,
        agency_rule="INFORM_AND_CONNECT; DO_NOT_DECIDE_FOR_PEOPLE",
        safety_rule="PRIORITIZE_IMMEDIATE_SAFETY_AND_APPROPRIATE_HUMAN_OR_EMERGENCY_SUPPORT",
        verification_rule="SOURCE -> CROSS_CHECK -> CONTEXT -> UNCERTAINTY -> AUTHORIZED_ACTION -> OUTCOME",
    )

def analyze_observation(observation: WorldObservation) -> dict[str, Any]:
    kind = observation.event_type if observation.event_type in EVENT_TYPES else classify_text(
        observation.title + " " + observation.summary
    )
    plan = build_humanitarian_plan(kind)
    return {
        "observation": observation.to_dict(),
        "classification": {
            "event_type": kind,
            "classification_is_not_fact": True,
            "evidence_status": observation.evidence_status,
            "confidence": observation.confidence,
        },
        "humanitarian_plan": plan.to_dict(),
        "historical_comparison": {
            "status": "REQUIRES_VERIFIED_HISTORICAL_EVIDENCE",
            "rule": "Compare analogous events and outcomes only after source verification.",
        },
        "nonviolence": {
            "default": True,
            "rule": "Never recommend retaliation, dehumanization or collective punishment.",
        },
        "external_action": {
            "status": "HUMAN_AUTHORIZATION_REQUIRED",
            "prohibited_by_default": [
                "autonomous_donations", "autonomous_government_contact",
                "autonomous_diplomatic_commitments", "surveillance_without_authorization",
            ],
        },
    }

def should_enter_world_pulse(message: str) -> bool:
    value = str(message or "").casefold()
    terms = (
        "מלחמה", "סכסוך", "מרד", "מחאה", "אסון", "רעידת", "הצפה", "שריפה",
        "משבר", "פליטים", "רעב", "מה קורה בעולם", "חדשות", "עולם", "מדינה",
        "war", "conflict", "uprising", "protest", "disaster", "crisis",
        "refugee", "famine", "what is happening", "world", "country",
    )
    return any(t in value for t in terms)

def compose_world_pulse_instruction() -> str:
    return (
        "[IMA WORLD PULSE] "
        "When the user asks about current world changes, conflicts, uprisings, disasters, "
        "political shifts, social movements, technological/scientific revolutions or a "
        "humanitarian situation: distinguish current evidence from interpretation; identify "
        "place/time/source; consider affected people and immediate needs; compare relevant "
        "historical outcomes only when verified; prefer nonviolent de-escalation and practical "
        "humanitarian support; never generalize guilt to a population; never claim live global "
        "coverage unless connected sources actually provide it; preserve human agency and "
        "require authorization for consequential external action."
    )
