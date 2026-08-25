from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

BASE = Path(__file__).resolve().parents[2]
MEDA = BASE / "external" / "MEDA"
RESEARCH_MEMORY = MEDA / "sessions" / "ima_research_memory.jsonl"


def _now() -> str:
    return datetime.now().isoformat()


def _safe_float(value: Any):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def extract_result(result: dict) -> dict:
    """
    Normalize a MEDA result into an IMA research/evidence record.

    This does not modify MEDA and does not replace IMA memory.
    It creates a stable boundary representation that can be learned from.
    """
    best_equations = result.get("best_equations", {})

    equations = {}
    if isinstance(best_equations, dict):
        for equation, payload in best_equations.items():
            if isinstance(payload, dict):
                equations[equation] = payload
            else:
                equations[equation] = {"value": payload}

    record = {
        "record_type": "meda_discovery",
        "source": "MEDA",
        "created_at": _now(),

        "mode": result.get("mode"),
        "selected_family_id": result.get("selected_family_id"),

        "best_fitness": _safe_float(result.get("best_fitness")),
        "constraint_score": _safe_float(result.get("constraint_score")),
        "hard_constraint_score": _safe_float(
            result.get("hard_constraint_score")
        ),
        "data_score": _safe_float(result.get("data_score")),
        "rmse": _safe_float(result.get("rmse")),
        "regularization_reward": _safe_float(
            result.get("regularization_reward")
        ),

        "hard_pass": bool(result.get("hard_pass", False)),
        "failed_constraints": result.get("failed_constraints", []),
        "hard_failed_constraints": result.get(
            "hard_failed_constraints", []
        ),

        "equations": equations,
        "n_nonzero_terms": result.get("n_nonzero_terms", {}),
        "constraint_scores": result.get("constraint_scores", {}),
        "integration_failures": result.get(
            "integration_failures", {}
        ),

        "top_candidates": result.get("top_candidates", []),
        "model_families": result.get("model_families", []),
        "seed_baseline_scores": result.get(
            "seed_baseline_scores", []
        ),

        "selection_reason": result.get("selection_reason"),
    }

    return record


def _concepts(record: dict) -> list[str]:
    concepts = ["scientific_discovery", "dynamical_system", "ODE"]

    mode = record.get("mode")
    if mode:
        concepts.append(f"meda_mode:{mode}")

    family = record.get("selected_family_id")
    if family:
        concepts.append(f"model_family:{family}")

    if record.get("hard_pass"):
        concepts.append("constraint_validated_model")

    equations = record.get("equations", {})
    for equation in equations:
        concepts.append(f"equation:{equation}")

    return concepts


def persist(record: dict) -> dict:
    """
    Durable local evidence ledger.

    JSONL is append-only so every MEDA discovery remains auditable.
    """
    RESEARCH_MEMORY.parent.mkdir(parents=True, exist_ok=True)

    with RESEARCH_MEMORY.open("a", encoding="utf-8") as f:
        f.write(
            json.dumps(
                record,
                ensure_ascii=False,
                separators=(",", ":"),
            )
            + "\n"
        )

    return {
        "ok": True,
        "path": str(RESEARCH_MEMORY),
        "concepts": _concepts(record),
    }


def learn_from_result(result: dict) -> dict:
    """
    MEDA -> IMA learning boundary.

    The primary durable artifact is the research evidence ledger.
    Universal learning is updated opportunistically if its API is usable.
    """
    record = extract_result(result)
    persisted = persist(record)

    learned = []

    try:
        from connectors.universal.universal_learning_engine import learn

        source = "MEDA"
        confidence = record.get("constraint_score")
        if confidence is None:
            confidence = 0.5

        for concept in _concepts(record):
            try:
                learn(
                    "scientific_discovery",
                    concept,
                    source,
                    float(confidence),
                )
                learned.append(concept)
            except Exception:
                # One learning failure must not destroy the MEDA result.
                pass

    except Exception:
        # The evidence ledger remains authoritative even if the
        # optional universal-learning adapter is unavailable.
        pass

    return {
        **persisted,
        "learned_concepts": learned,
        "record": record,
    }


def receive_file(path: str | Path) -> dict:
    path = Path(path)

    if not path.is_absolute():
        path = BASE / path

    if not path.is_file():
        return {
            "ok": False,
            "error": "result_file_not_found",
            "path": str(path),
        }

    try:
        result = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {
            "ok": False,
            "error": "invalid_result_json",
            "message": str(exc),
            "path": str(path),
        }

    learned = learn_from_result(result)
    learned["result_path"] = str(path)
    return learned


def recent(limit: int = 10) -> list[dict]:
    if not RESEARCH_MEMORY.is_file():
        return []

    rows = []
    for line in RESEARCH_MEMORY.read_text(
        encoding="utf-8"
    ).splitlines():
        try:
            rows.append(json.loads(line))
        except Exception:
            continue

    return rows[-max(1, int(limit)):]
