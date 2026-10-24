"""IMA creator-question memory: capture questions without turning them into facts."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import json
from typing import Any

REGISTRY = Path("learning/questions/IMA_CREATOR_QUESTION_REGISTRY.json")


@dataclass(frozen=True)
class CreatorQuestion:
    id: str
    question: str
    source: str
    observed_at: str
    attribution: str = "ORI_AUTHORED"
    status: str = "OPEN"
    related_ids: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()


def validate_timestamp(value: str) -> bool:
    """Require an authoritative ISO-8601 timestamp/date; never synthesize missing time."""
    if len(value) == 10:
        try:
            datetime.fromisoformat(value)
            return True
        except ValueError:
            return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return "T" in value
    except ValueError:
        return False


def record_question(
    question: str,
    source: str,
    observed_at: str,
    *,
    question_id: str,
    attribution: str = "ORI_AUTHORED",
    status: str = "OPEN",
    related_ids: tuple[str, ...] = (),
    tags: tuple[str, ...] = (),
) -> dict[str, Any]:
    if not question.strip():
        raise ValueError("question must not be empty")
    if not validate_timestamp(observed_at):
        raise ValueError("observed_at must be an authoritative ISO-8601 date/time")
    if attribution not in {
        "ORI_AUTHORED",
        "QUOTED_SOURCE",
        "IMA_GENERATED",
        "RESEARCH_DERIVED",
        "TEST_FALSIFICATION",
    }:
        raise ValueError("invalid attribution")
    if status not in {"OPEN", "SUPPORTED", "REJECTED", "INCONCLUSIVE"}:
        raise ValueError("invalid question status")

    return asdict(CreatorQuestion(
        id=question_id,
        question=question,
        source=source,
        observed_at=observed_at,
        attribution=attribution,
        status=status,
        related_ids=related_ids,
        tags=tags,
    ))


def load_registry(path: Path = REGISTRY) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def find_related_questions(question: str, registry: dict[str, Any]) -> list[dict[str, Any]]:
    """Small deterministic lexical bridge; semantic matching belongs above this layer."""
    terms = {t.lower() for t in question.split() if len(t) > 2}
    results = []
    for item in registry.get("seeded_recovered_questions", []):
        overlap = len(terms & {t.lower() for t in item["question"].split()})
        if overlap:
            results.append(item)
    return results


def question_memory_contract() -> dict[str, Any]:
    return {
        "schema": "IMA-CREATOR-QUESTIONS-1.0",
        "captures_user_questions": True,
        "preserves_provenance": True,
        "requires_authoritative_timestamp": True,
        "zero_point_protocol": "research/IMA_ZERO_POINT_DISCOVERY_PROTOCOL.json",
        "private_by_default": True,
        "future_question_generation": True,
        "author_attribution_separated": True,
    }
