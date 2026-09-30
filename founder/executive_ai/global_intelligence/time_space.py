"""IMA Time & Space Intelligence primitives.

Cross-cutting normalization only: no tracking, trading, or autonomous authority.
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

SCHEMA_VERSION = "ima-time-space-1"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize(
    *,
    observed_at: str | None = None,
    valid_from: str | None = None,
    valid_until: str | None = None,
    location: Any = None,
    location_uncertainty: Any = None,
    source: str | None = None,
    source_timestamp: str | None = None,
    measurement_type: str | None = None,
    value: Any = None,
    unit: str | None = None,
    confidence: float | None = None,
    provenance: Any = None,
    constraints: Any = None,
    estimated_cost: Any = None,
    estimated_value: Any = None,
    latency: Any = None,
    risk: Any = None,
    human_authorization_required: bool = True,
    verification_state: str = "unverified",
) -> dict[str, Any]:
    """Return a provenance-preserving time-space record."""
    return {
        "schema_version": SCHEMA_VERSION,
        "observed_at": observed_at or now_iso(),
        "valid_from": valid_from,
        "valid_until": valid_until,
        "location": location,
        "location_uncertainty": location_uncertainty,
        "source": source,
        "source_timestamp": source_timestamp,
        "measurement_type": measurement_type,
        "value": value,
        "unit": unit,
        "confidence": confidence,
        "provenance": provenance,
        "constraints": constraints,
        "estimated_cost": estimated_cost,
        "estimated_value": estimated_value,
        "latency": latency,
        "risk": risk,
        "human_authorization_required": human_authorization_required,
        "verification_state": verification_state,
    }


def from_opportunity(
    *,
    source: str,
    source_timestamp: str | None = None,
    title: str = "",
    url: str | None = None,
    category: str = "general",
    observed_at: str | None = None,
    valid_from: str | None = None,
    valid_until: str | None = None,
    location: Any = None,
    location_uncertainty: Any = None,
    confidence: float | None = None,
    constraints: Any = None,
    estimated_cost: Any = None,
    estimated_value: Any = None,
    latency: Any = None,
    risk: Any = "unknown",
    verification_state: str = "public-source-unverified",
) -> dict[str, Any]:
    return normalize(
        observed_at=observed_at,
        valid_from=valid_from,
        valid_until=valid_until,
        location=location,
        location_uncertainty=location_uncertainty,
        source=source,
        source_timestamp=source_timestamp,
        measurement_type="opportunity_signal",
        value={"title": title, "url": url, "category": category},
        confidence=confidence,
        provenance={"source": source, "url": url},
        constraints=constraints,
        estimated_cost=estimated_cost,
        estimated_value=estimated_value,
        latency=latency,
        risk=risk,
        human_authorization_required=True,
        verification_state=verification_state,
    )
def validate(record: dict[str, Any]) -> tuple[bool, list[str]]:
    """Validate the minimum evidence needed for consequential use."""
    errors: list[str] = []
    if not record.get("schema_version"):
        errors.append("missing_schema_version")
    if not record.get("observed_at"):
        errors.append("missing_observed_at")
    if not record.get("source"):
        errors.append("missing_source")
    if record.get("confidence") is not None:
        try:
            c = float(record["confidence"])
            if c < 0 or c > 100:
                errors.append("confidence_out_of_range")
        except (TypeError, ValueError):
            errors.append("confidence_not_numeric")
    if record.get("human_authorization_required") is not True:
        errors.append("authorization_flag_must_remain_true")
    return not errors, errors


def opportunity_dimensions(record: dict[str, Any]) -> dict[str, Any]:
    """Stable dimensions for graph matching and future sensor adapters."""
    return {
        "time": {
            "observed_at": record.get("observed_at"),
            "valid_from": record.get("valid_from"),
            "valid_until": record.get("valid_until"),
            "source_timestamp": record.get("source_timestamp"),
            "latency": record.get("latency"),
        },
        "space": {
            "location": record.get("location"),
            "location_uncertainty": record.get("location_uncertainty"),
        },
        "evidence": {
            "source": record.get("source"),
            "provenance": record.get("provenance"),
            "verification_state": record.get("verification_state"),
            "confidence": record.get("confidence"),
        },
    }
