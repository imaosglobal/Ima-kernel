"""Canonical human-approval contract for consequential actions."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ApprovalDecision:
    action_id: str
    status: str
    reason: str


def evaluate_approval(*, action_id: str, consequential: bool, confirmed: bool) -> ApprovalDecision:
    if not action_id:
        return ApprovalDecision("", "REJECTED", "missing_action_id")
    if not consequential:
        return ApprovalDecision(action_id, "ALLOWED", "non_consequential")
    if confirmed:
        return ApprovalDecision(action_id, "ALLOWED", "explicit_user_confirmation")
    return ApprovalDecision(action_id, "BLOCKED", "explicit_user_confirmation_required")
