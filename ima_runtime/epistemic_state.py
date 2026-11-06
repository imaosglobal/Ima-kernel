from __future__ import annotations
from typing import Any, Iterable, Mapping

TRUTH_STATES = (
    "ESTABLISHED_FACT",
    "SUPPORTED_FINDING",
    "OPEN_HYPOTHESIS",
    "INTERPRETATION",
    "METAPHOR",
    "UNKNOWN",
)

_EXPLICIT = {s.lower(): s for s in TRUTH_STATES}

def _clean(value: Any) -> str:
    return str(value or "").strip()

def _items(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, (list, tuple, set, frozenset)):
        return [_clean(x) for x in value if _clean(x)]
    value = _clean(value)
    return [value] if value else []

def build_epistemic_record(
    response: str,
    *,
    evidence: Iterable[Any] = (),
    context: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build an evidence-bounded decision record without manufacturing certainty.

    Explicit truth state is accepted only when it is one of the canonical states.
    Otherwise the record stays UNKNOWN unless verification/evidence supplied by the
    caller justifies promotion. This is a child component of the canonical
    reflection runtime, not a second authority.
    """
    ctx = dict(context or {})
    ev = _items(evidence)
    requested = _EXPLICIT.get(_clean(ctx.get("truth_state")).lower())
    verified = bool(ctx.get("verified") is True)

    if requested:
        state = requested
    elif verified and ev:
        state = "ESTABLISHED_FACT"
    elif ev:
        state = "SUPPORTED_FINDING"
    else:
        state = "UNKNOWN"

    test = _clean(ctx.get("testable") or ctx.get("proposed_next_step"))
    if not test and state in {"OPEN_HYPOTHESIS", "UNKNOWN"}:
        test = "Identify the smallest useful evidence or test before increasing certainty."

    return {
        "schema": "IMA-EPISTEMIC-DECISION-1.0",
        "truth_state": state,
        "known": _clean(ctx.get("known")),
        "unknown": _items(ctx.get("unknown")) or ([] if state != "UNKNOWN" else ["The claim is not sufficiently evidenced for a stronger truth state."]),
        "test": test,
        "interpretation": _clean(ctx.get("interpretation")),
        "hypothesis": _clean(ctx.get("hypothesis")),
        "metaphor": _clean(ctx.get("metaphor")),
        "meaning": _clean(ctx.get("meaning")),
        "human_choice": _clean(ctx.get("human_choice")),
        "feedback": _items(ctx.get("feedback")),
        "learning": _clean(ctx.get("learning")),
        "evidence": ev,
        "claim": _clean(response),
    }
