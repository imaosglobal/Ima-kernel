"""Canonical provider-neutral IMA intelligence interoperability registry helpers.

This module validates lifecycle evidence only. It never creates credentials,
connects providers, or executes cross-provider actions by itself.
"""

from __future__ import annotations

LIFECYCLE = (
    "DISCOVERED",
    "ELIGIBLE",
    "ADAPTER-READY",
    "AUTHORIZED",
    "CONNECTED",
    "RUNTIME-VERIFIED",
    "MONITORED",
)

REQUIRED_PROGRESS = {
    "CONNECTED": {"authorized_credentials_or_explicit_host_permission", "successful_connection_evidence"},
    "RUNTIME-VERIFIED": {"successful_live_request_or_interaction", "captured_result_evidence", "boundary_check"},
    "MONITORED": {"runtime_verified", "repeatable_health_check"},
}


def validate_candidate(candidate: dict) -> list[str]:
    """Return evidence gaps for the candidate's declared lifecycle state."""
    status = candidate.get("status")
    if status not in LIFECYCLE:
        return [f"invalid_status:{status}"]

    evidence = set(candidate.get("evidence_tags", []))
    gaps: list[str] = []

    for tag in REQUIRED_PROGRESS.get(status, set()):
        if tag not in evidence:
            gaps.append(f"missing:{tag}")

    if status in {"CONNECTED", "RUNTIME-VERIFIED", "MONITORED"}:
        if not candidate.get("authorization"):
            gaps.append("missing:authorization_record")

    if status in {"RUNTIME-VERIFIED", "MONITORED"} and not candidate.get("live_result_evidence"):
        gaps.append("missing:live_result_evidence")

    if status == "MONITORED" and not candidate.get("health_check_evidence"):
        gaps.append("missing:health_check_evidence")

    return gaps


def promote(candidate: dict, target_status: str) -> dict:
    """Return a copy with a status only when the required evidence is present."""
    if target_status not in LIFECYCLE:
        raise ValueError(f"invalid_status:{target_status}")
    idx = LIFECYCLE.index(target_status)
    current = candidate.get("status")
    if current not in LIFECYCLE or LIFECYCLE.index(current) > idx:
        raise ValueError("lifecycle_regression_or_invalid_current_status")

    proposed = dict(candidate, status=target_status)
    gaps = validate_candidate(proposed)
    if gaps:
        raise ValueError(";".join(gaps))
    return proposed
