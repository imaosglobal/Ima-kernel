"""Evidence-only quality guard migrated from the legacy evolving-home quality system.

This module deliberately does not mutate the product, attach event handlers, reload pages,
or run background timers. It converts observed QA signals into deterministic findings so
the canonical IMA QA/deployment loop can decide what to do.

Legacy provenance: imaosglobal/ima-os-evolving-home/PERMANENT_QUALITY_SYSTEM.md
"""
from dataclasses import dataclass
from typing import Iterable, Mapping


@dataclass(frozen=True)
class QualityFinding:
    area: str
    status: str
    detail: str
    severity: str = "info"


REQUIRED_AREAS = (
    "buttons",
    "authentication",
    "pwa",
    "accessibility",
    "performance",
    "security",
    "routing",
)


def evaluate_quality_signals(
    signals: Mapping[str, bool],
    *,
    required_areas: Iterable[str] = REQUIRED_AREAS,
) -> list[QualityFinding]:
    """Turn observed QA signals into findings without performing side effects.

    Missing signals are reported as NOT_OBSERVED rather than inferred as failures.
    A false signal is reported as FAILED. A true signal is PASSED.
    """
    findings: list[QualityFinding] = []

    for area in required_areas:
        if area not in signals:
            findings.append(
                QualityFinding(
                    area=area,
                    status="NOT_OBSERVED",
                    detail="No verified observation was supplied.",
                    severity="warning",
                )
            )
            continue

        passed = bool(signals[area])
        findings.append(
            QualityFinding(
                area=area,
                status="PASSED" if passed else "FAILED",
                detail="Verified observation supplied by the QA surface.",
                severity="info" if passed else "error",
            )
        )

    return findings


def quality_summary(findings: Iterable[QualityFinding]) -> dict[str, int | bool]:
    """Return deterministic summary counts for the canonical QA journal."""
    items = list(findings)
    failed = sum(item.status == "FAILED" for item in items)
    missing = sum(item.status == "NOT_OBSERVED" for item in items)
    passed = sum(item.status == "PASSED" for item in items)

    return {
        "passed": passed,
        "failed": failed,
        "not_observed": missing,
        "healthy": failed == 0 and missing == 0,
    }
