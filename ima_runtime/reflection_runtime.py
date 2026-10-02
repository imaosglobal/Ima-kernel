"""Live integration point for IMA's reflection protocol."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable, Optional

from .reflection_gap_closure import Conclusion, compare, close_gaps, to_record

ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT / ".ima" / "reflection"
STATE_FILE = STATE_DIR / "reflection.jsonl"

def reflect(
    response: str,
    *,
    evidence: tuple = (),
    independent: Optional[Conclusion] = None,
    verifier: Optional[Callable[[Any, str], Any]] = None,
    context: Optional[dict] = None,
) -> dict:
    """Run the reflection gate for a live IMA response.

    Missing independent reasoning is recorded as TRUE_UNKNOWN rather than
    silently treating IMA's first conclusion as verified truth.
    """
    ima = Conclusion(
        claim=str(response or "").strip(),
        evidence=tuple(evidence or ()),
        assumptions=tuple((context or {}).get("assumptions", ())),
        uncertainty=str((context or {}).get("uncertainty", "")),
        proposed_next_step=str((context or {}).get("proposed_next_step", "")),
        objective=str((context or {}).get("objective", "")),
        scope=str((context or {}).get("scope", "")),
        capability=str((context or {}).get("capability", "")),
        values=tuple((context or {}).get("values", ())),
    )
    comparison = compare(ima, independent)
    comparison = close_gaps(comparison, verifier)
    record = {
        "schema": "IMA-REFLECTION-RUNTIME-1.0",
        "comparison": to_record(comparison),
    }
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    with STATE_FILE.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False, sort_keys=True, default=str) + "\n")
    return record
