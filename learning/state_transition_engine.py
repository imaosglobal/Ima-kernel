"""
IMA State Transition Engine

Purpose:
    Observe conversational state transitions from observable input/context.

Design principles:
    - Observation != inference
    - Inference != hypothesis
    - Hypothesis != prediction
    - Prediction != outcome
    - No diagnosis
    - No hidden-state claims
    - No independent user-memory store
    - Append-only event journal
    - Compatible with existing IMA learning/runtime infrastructure
"""

from __future__ import annotations

from collections import Counter
from datetime import datetime
from pathlib import Path
import hashlib
import json
import math
import re
from typing import Any, Dict, List


ROOT = Path(".")
EVENT_FILE = ROOT / "learning" / "state_transition_events.jsonl"


# ------------------------------------------------------------
# Observable linguistic features
# ------------------------------------------------------------

HEBREW_RE = re.compile(r"[\u0590-\u05FF]")
QUESTION_RE = re.compile(r"[?？]")
EXCLAMATION_RE = re.compile(r"[!！]")
NEWLINE_RE = re.compile(r"\n+")


def _safe_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


def _tokenize(text: str) -> List[str]:
    return re.findall(r"\S+", text.lower())


def _unique_ratio(tokens: List[str]) -> float:
    if not tokens:
        return 0.0
    return len(set(tokens)) / len(tokens)


def _sentence_count(text: str) -> int:
    if not text.strip():
        return 0
    parts = re.split(r"[.!?。！？]+", text)
    return max(1, len([x for x in parts if x.strip()]))


def _feature_vector(text: str) -> Dict[str, float]:
    tokens = _tokenize(text)
    chars = len(text)
    words = len(tokens)

    question_count = len(QUESTION_RE.findall(text))
    exclamation_count = len(EXCLAMATION_RE.findall(text))

    lines = [x for x in NEWLINE_RE.split(text) if x.strip()]

    return {
        "char_count": float(chars),
        "word_count": float(words),
        "sentence_count": float(_sentence_count(text)),
        "question_marks": float(question_count),
        "exclamation_marks": float(exclamation_count),
        "question_density": (
            question_count / max(1, words)
        ),
        "newline_density": (
            max(0, len(lines) - 1) / max(1, words)
        ),
        "unique_token_ratio": _unique_ratio(tokens),
        "hebrew_ratio": (
            len(HEBREW_RE.findall(text)) / max(1, chars)
        ),
        "uppercase_ratio": (
            sum(1 for c in text if c.isupper())
            / max(1, sum(1 for c in text if c.isalpha()))
        ),
    }


# ------------------------------------------------------------
# Observable state classification
# ------------------------------------------------------------

def _classify_state(features: Dict[str, float], text: str) -> Dict[str, Any]:
    """
    Conversational state, not psychological diagnosis.

    These labels describe the observable interaction mode.
    """

    q = features["question_density"]
    length = features["word_count"]
    sentences = features["sentence_count"]

    if length < 8:
        label = "brief"
    elif q >= 0.12:
        label = "inquiry"
    elif sentences >= 8 or length >= 120:
        label = "extended_expression"
    elif features["unique_token_ratio"] >= 0.78:
        label = "exploration"
    else:
        label = "discussion"

    return {
        "label": label,
        "observable": True,
        "features": features,
    }


# ------------------------------------------------------------
# Observable factors
# ------------------------------------------------------------

def _factors(text: str, features: Dict[str, float]) -> List[Dict[str, Any]]:
    factors = []

    if features["question_density"] > 0:
        factors.append({
            "name": "questioning",
            "value": features["question_density"],
            "source": "text",
        })

    if features["word_count"] >= 80:
        factors.append({
            "name": "high_text_volume",
            "value": min(1.0, features["word_count"] / 250.0),
            "source": "text",
        })

    if features["sentence_count"] >= 6:
        factors.append({
            "name": "multi_sentence_structure",
            "value": min(1.0, features["sentence_count"] / 15.0),
            "source": "text",
        })

    if features["unique_token_ratio"] >= 0.75:
        factors.append({
            "name": "lexical_exploration",
            "value": features["unique_token_ratio"],
            "source": "text",
        })

    if features["exclamation_marks"] > 0:
        factors.append({
            "name": "explicit_emphasis",
            "value": min(1.0, features["exclamation_marks"] / 3.0),
            "source": "text",
        })

    return factors


# ------------------------------------------------------------
# Transition hypotheses
# ------------------------------------------------------------

def _transition_hypotheses(previous_state: Dict[str, Any] | None,
                           current_state: Dict[str, Any],
                           factors: List[Dict[str, Any]]) -> List[Dict[str, Any]]:

    current = current_state["label"]

    if previous_state is None:
        return [{
            "from": None,
            "to": current,
            "kind": "initial_observation",
            "confidence": 0.35,
            "evidence": ["no_previous_observation"],
        }]

    previous = previous_state.get("label", "unknown")

    if previous == current:
        return [{
            "from": previous,
            "to": current,
            "kind": "persistence",
            "confidence": 0.60,
            "evidence": ["same_observable_state"],
        }]

    evidence = [
        f"previous={previous}",
        f"current={current}",
    ]

    if factors:
        evidence.extend(
            f"factor={x['name']}"
            for x in factors
        )

    return [{
        "from": previous,
        "to": current,
        "kind": "observed_transition",
        "confidence": 0.55,
        "evidence": evidence,
    }]


def _prediction(previous_state: Dict[str, Any] | None,
                current_state: Dict[str, Any],
                factors: List[Dict[str, Any]]) -> Dict[str, Any]:

    current = current_state["label"]

    # Conservative first-generation prediction.
    # It predicts interaction mode, not a person's internal state.
    if current == "inquiry":
        candidates = [
            ("inquiry", 0.42),
            ("discussion", 0.30),
            ("extended_expression", 0.18),
            ("brief", 0.10),
        ]
    elif current == "extended_expression":
        candidates = [
            ("extended_expression", 0.38),
            ("discussion", 0.32),
            ("inquiry", 0.20),
            ("brief", 0.10),
        ]
    elif current == "exploration":
        candidates = [
            ("exploration", 0.40),
            ("inquiry", 0.30),
            ("discussion", 0.20),
            ("extended_expression", 0.10),
        ]
    elif current == "brief":
        candidates = [
            ("brief", 0.40),
            ("inquiry", 0.30),
            ("discussion", 0.20),
            ("extended_expression", 0.10),
        ]
    else:
        candidates = [
            ("discussion", 0.45),
            ("inquiry", 0.25),
            ("exploration", 0.15),
            ("extended_expression", 0.15),
        ]

    return {
        "target": current,
        "candidates": [
            {"state": state, "probability": probability}
            for state, probability in candidates
        ],
        "method": "baseline_observable_transition_model",
        "learned": False,
    }


def _event_id(event: Dict[str, Any]) -> str:
    raw = json.dumps(
        event,
        ensure_ascii=False,
        sort_keys=True,
        default=str,
    )
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]


# ------------------------------------------------------------
# Public API
# ------------------------------------------------------------

def observe(
    text: str,
    context: Dict[str, Any] | None = None,
    response: str = "",
) -> Dict[str, Any]:

    text = _safe_text(text)
    context = context or {}

    features = _feature_vector(text)
    current_state = _classify_state(features, text)
    factors = _factors(text, features)

    previous_state = None

    history = context.get("history", [])
    if history:
        previous = history[-1]

        previous_text = (
            previous.get("question")
            or previous.get("message")
            or previous.get("text")
            or ""
        )

        if previous_text:
            previous_features = _feature_vector(
                _safe_text(previous_text)
            )
            previous_state = _classify_state(
                previous_features,
                _safe_text(previous_text),
            )

    transitions = _transition_hypotheses(
        previous_state,
        current_state,
        factors,
    )

    prediction = _prediction(
        previous_state,
        current_state,
        factors,
    )

    result = {
        "schema": "ima.state_transition.v1",
        "time": datetime.now().isoformat(),
        "observation": {
            "text_length": len(text),
            "features": features,
        },
        "state": current_state,
        "previous_state": previous_state,
        "factors": factors,
        "transition_hypotheses": transitions,
        "prediction": prediction,
        "outcome": {
            "observed": True,
            "response_length": len(_safe_text(response)),
            "next_state": None,
        },
        "context": {
            "history_count": len(history),
            "has_user": bool(context.get("user")),
        },
        "status": "observation_only",
    }

    result["_id"] = _event_id(result)

    return result


def record(result: Dict[str, Any]) -> Dict[str, Any]:
    EVENT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with EVENT_FILE.open("a", encoding="utf-8") as f:
        f.write(
            json.dumps(
                result,
                ensure_ascii=False,
                sort_keys=True,
            ) + "\n"
        )

    return result


def observe_and_record(
    text: str,
    context: Dict[str, Any] | None = None,
    response: str = "",
) -> Dict[str, Any]:

    result = observe(
        text=text,
        context=context,
        response=response,
    )

    return record(result)
