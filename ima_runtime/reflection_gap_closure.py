"""Runtime reflection, comparison, gap classification and evidence-gated closure for IMA.

This module does not manufacture agreement. It makes differences explicit and only
marks a gap resolved when a caller supplies new evidence/verification.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Callable, Iterable, Mapping, Optional, Tuple

GAP_TYPES = (
    "EVIDENCE_GAP",
    "INTERPRETATION_GAP",
    "ASSUMPTION_GAP",
    "OBJECTIVE_GAP",
    "SCOPE_GAP",
    "CAPABILITY_GAP",
    "UNCERTAINTY_GAP",
    "VALUE_GAP",
    "TRUE_UNKNOWN",
)

@dataclass(frozen=True)
class Conclusion:
    claim: str
    evidence: tuple = ()
    assumptions: tuple = ()
    uncertainty: str = ""
    proposed_next_step: str = ""
    objective: str = ""
    scope: str = ""
    capability: str = ""
    values: tuple = ()

@dataclass(frozen=True)
class Comparison:
    ima: Conclusion
    independent: Optional[Conclusion]
    agreement: bool
    differences: tuple
    gap_types: tuple
    resolution_status: str
    explanation: tuple = ()

    @property
    def unresolved(self) -> bool:
        return self.resolution_status not in {"AGREEMENT", "RESOLVED"}

def _tuple(value: Any) -> tuple:
    if value is None:
        return ()
    if isinstance(value, tuple):
        return value
    if isinstance(value, (list, set, frozenset)):
        return tuple(value)
    return (value,)

def _gap_for_claim(a: Conclusion, b: Conclusion) -> str:
    if a.evidence != b.evidence:
        return "EVIDENCE_GAP"
    if a.objective != b.objective:
        return "OBJECTIVE_GAP"
    if a.scope != b.scope:
        return "SCOPE_GAP"
    if a.capability != b.capability:
        return "CAPABILITY_GAP"
    if a.values != b.values:
        return "VALUE_GAP"
    if a.assumptions != b.assumptions:
        return "ASSUMPTION_GAP"
    return "INTERPRETATION_GAP"

def compare(ima: Conclusion, independent: Optional[Conclusion]) -> Comparison:
    if independent is None:
        return Comparison(
            ima=ima,
            independent=None,
            agreement=False,
            differences=("independent_conclusion_missing",),
            gap_types=("TRUE_UNKNOWN",),
            resolution_status="UNRESOLVED",
            explanation=("No independent conclusion was supplied; agreement must not be inferred.",),
        )

    differences = []
    gaps = []
    explanation = []

    if ima.claim != independent.claim:
        differences.append("claim")
        gaps.append(_gap_for_claim(ima, independent))
        explanation.append("The claims differ; the cause is classified from evidence and context fields.")
    for field, gap in (
        ("assumptions", "ASSUMPTION_GAP"),
        ("objective", "OBJECTIVE_GAP"),
        ("scope", "SCOPE_GAP"),
        ("capability", "CAPABILITY_GAP"),
        ("values", "VALUE_GAP"),
        ("uncertainty", "UNCERTAINTY_GAP"),
        ("evidence", "EVIDENCE_GAP"),
        ("proposed_next_step", "INTERPRETATION_GAP"),
    ):
        if getattr(ima, field) != getattr(independent, field):
            differences.append(field)
            gaps.append(gap)

    unique_gaps = tuple(dict.fromkeys(gaps))
    return Comparison(
        ima=ima,
        independent=independent,
        agreement=not differences,
        differences=tuple(dict.fromkeys(differences)),
        gap_types=unique_gaps,
        resolution_status="AGREEMENT" if not differences else "UNRESOLVED",
        explanation=tuple(explanation),
    )

def close_gaps(
    comparison: Comparison,
    verifier: Optional[Callable[[Comparison, str], Any]] = None,
) -> Comparison:
    """Attempt closure only through caller-supplied verification.

    The verifier receives (comparison, gap_type) and must return truthy evidence.
    No verifier means the gaps remain unresolved.
    """
    if not comparison.unresolved:
        return comparison
    if verifier is None:
        return comparison

    remaining = []
    closed = []
    for gap in comparison.gap_types:
        try:
            result = verifier(comparison, gap)
        except Exception:
            result = False
        if result:
            closed.append(gap)
        else:
            remaining.append(gap)

    if not remaining and closed:
        return Comparison(
            ima=comparison.ima,
            independent=comparison.independent,
            agreement=comparison.agreement,
            differences=comparison.differences,
            gap_types=(),
            resolution_status="RESOLVED",
            explanation=comparison.explanation + (f"Verified closure: {','.join(closed)}.",),
        )
    return Comparison(
        ima=comparison.ima,
        independent=comparison.independent,
        agreement=comparison.agreement,
        differences=comparison.differences,
        gap_types=tuple(remaining),
        resolution_status="PARTIALLY_RESOLVED" if closed else "UNRESOLVED",
        explanation=comparison.explanation + (f"Verified closure: {','.join(closed)}." if closed else "No gap was verified as closed.",),
    )

def conclusion_from_result(response: str, *, evidence: Iterable[Any] = (), **fields: Any) -> Conclusion:
    return Conclusion(claim=str(response or "").strip(), evidence=_tuple(evidence), **fields)

def to_record(comparison: Comparison) -> dict:
    return asdict(comparison)

def self_test() -> dict:
    a = Conclusion("same", ("fact",), uncertainty="low", proposed_next_step="verify")
    assert compare(a, a).agreement

    b = Conclusion("different", ("other",), uncertainty="low", proposed_next_step="verify")
    r = compare(a, b)
    assert not r.agreement and "EVIDENCE_GAP" in r.gap_types
    assert r.resolution_status == "UNRESOLVED"

    missing = compare(a, None)
    assert "TRUE_UNKNOWN" in missing.gap_types

    closed = close_gaps(r, lambda _c, gap: gap == "EVIDENCE_GAP")
    assert closed.resolution_status == "RESOLVED" and closed.gap_types == ()
    return {"ok": True, "agreement": to_record(compare(a, a)), "gap": to_record(r), "unknown": to_record(missing)}

if __name__ == "__main__":
    print(self_test())
