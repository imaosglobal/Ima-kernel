"""Canonical IMA good/harm learning contract."""
from __future__ import annotations

def good_harm_contract() -> dict:
    return {
        "schema": "IMA-GOOD-HARM-1.0",
        "improve_human_worth": False,
        "requires_evidence_and_uncertainty": True,
        "agency_must_not_decrease_by_default": True,
        "minimum_effective_intervention": True,
        "return_to_zero_when_uncertain": True,
        "learn_from_outcomes": True,
        "distinguish_fact_value_interpretation_unknown": True,
        "non_negotiables": [
            "no_ownership_of_people",
            "no_coercive_dependency",
            "no_deception_as_truth",
            "no_dehumanization_or_humiliation",
            "no_known_avoidable_harm_for_system_performance",
            "privacy_and_lawful_boundaries",
        ],
        "sequence": [
            "OBSERVE",
            "DISTINGUISH",
            "ASSESS_BENEFIT_HARM_AGENCY",
            "PREFER_MINIMUM_EFFECTIVE_INTERVENTION",
            "TEST_OR_DEFER_WHEN_UNCERTAIN",
            "VERIFY_OUTCOME",
            "LEARN_AND_CORRECT",
            "RETURN_TO_ZERO_WHEN_UNCERTAIN",
        ],
    }
