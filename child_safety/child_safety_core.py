"""Compatibility adapter for the canonical IMA child-safety engine.

Do not add a second safety policy here. All checks delegate to
learning.child_safety_engine so older callers receive the same enforcement
decisions as the public chat runtime.
"""
from learning.child_safety_engine import evaluate_interaction


class ChildSafetyCore:
    def evaluate(self, context):
        context = context if isinstance(context, dict) else {}
        result = evaluate_interaction(
            age_band=str(context.get("age_band", "unknown")),
            user_message=str(context.get("user_message", "")),
            assistant_response=str(context.get("assistant_response", "")),
        )
        return {
            **result,
            "safe": bool(result["allowed"] and not result["requires_human_review"]),
            "mode": "child_protection",
            "canonical_engine": "learning.child_safety_engine",
        }
