"""Continuous worldview expansion orchestration for IMA.

This module creates a bounded, auditable research pass. It does not pretend
that unavailable tools, people, sources, or models were consulted.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, Optional

from .development_journal import record as journal_record

ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT / ".ima" / "worldview"
STATE_FILE = STATE_DIR / "expansion.jsonl"


@dataclass(frozen=True)
class SourceResult:
    source_id: str
    kind: str
    status: str
    claims: tuple[str, ...] = ()
    provenance: tuple[str, ...] = ()
    uncertainty: str = ""
    error: str = ""


@dataclass(frozen=True)
class ExpansionRecord:
    schema: str
    timestamp: str
    question: str
    sources_considered: tuple[str, ...]
    sources_consulted: tuple[str, ...]
    unavailable_sources: tuple[str, ...]
    results: tuple[SourceResult, ...]
    gaps: tuple[str, ...]
    next_checks: tuple[str, ...]


Provider = Callable[[str], SourceResult]


def expand(
    question: str,
    providers: Iterable[tuple[str, str, Provider]] = (),
    *,
    required_kinds: Iterable[str] = (),
    context: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """Run one bounded expansion pass and persist exactly what was checked.

    Providers are explicit adapters. A provider is consulted only when the
    caller actually supplies it; unavailable capabilities remain visible.
    """
    q = str(question or "").strip()
    if not q:
        raise ValueError("question must not be empty")

    required = set(str(x) for x in required_kinds)
    declared = list(providers)
    results: list[SourceResult] = []
    considered: list[str] = []
    consulted: list[str] = []
    unavailable: list[str] = []

    for source_id, kind, provider in declared:
        considered.append(source_id)
        try:
            result = provider(q)
            if not isinstance(result, SourceResult):
                result = SourceResult(source_id, kind, "INVALID_PROVIDER_RESULT", error="provider returned a non-SourceResult")
        except Exception as exc:  # provider failures must become evidence, not hidden state
            result = SourceResult(source_id, kind, "ERROR", error=f"{type(exc).__name__}: {exc}")
        results.append(result)
        if result.status == "CONSULTED":
            consulted.append(source_id)
        else:
            unavailable.append(source_id)

    present_kinds = {r.kind for r in results if r.status == "CONSULTED"}
    gaps = []
    if required - present_kinds:
        gaps.append("MISSING_REQUIRED_SOURCE_KINDS:" + ",".join(sorted(required - present_kinds)))
    if not consulted:
        gaps.append("TRUE_UNKNOWN:NO_SOURCE_WAS_ACTUALLY_CONSULTED")
    if any(r.status in {"ERROR", "INVALID_PROVIDER_RESULT"} for r in results):
        gaps.append("SOURCE_EXECUTION_GAP")

    next_checks = [
        "seek primary evidence where available",
        "check an independent reasoning path",
        "look for counterexamples and missing perspectives",
        "recheck after new evidence or tools become available",
    ]
    if context and context.get("next_checks"):
        next_checks.extend(str(x) for x in context["next_checks"])

    record = ExpansionRecord(
        schema="IMA-WORLDVIEW-EXPANSION-1.0",
        timestamp=datetime.now(timezone.utc).isoformat(),
        question=q,
        sources_considered=tuple(considered),
        sources_consulted=tuple(consulted),
        unavailable_sources=tuple(unavailable),
        results=tuple(results),
        gaps=tuple(gaps),
        next_checks=tuple(dict.fromkeys(next_checks)),
    )
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    with STATE_FILE.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(asdict(record), ensure_ascii=False, sort_keys=True, default=str) + "\n")
    journal_record(
        "WORLDVIEW_EXPANSION",
        q,
        source="ima_runtime.worldview_expansion",
        status="VERIFIED" if not gaps else "GAPS_RECORDED",
        details={"sources_consulted": consulted, "gaps": gaps},
    )
    return asdict(record)


def self_test() -> bool:
    result = expand(
        "IMA worldview expansion self-test",
        [("self-test", "test", lambda q: SourceResult("self-test", "test", "CONSULTED", (q,), ("runtime",)))],
        required_kinds=("test",),
    )
    return result["sources_consulted"] == ["self-test"] and not result["gaps"]
