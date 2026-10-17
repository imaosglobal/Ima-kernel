"""IMA Trend-to-Brand Engine.

Evidence-first research capability inspired only by public business patterns.
It consumes permitted public evidence, separates facts/estimates/hypotheses,
and never performs commerce or outreach.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STATE = ROOT / ".ima/web_intelligence/trend_to_brand_state.json"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:20]


def _bounded(value: object, default: float = 0.0) -> float:
    try:
        return min(1.0, max(0.0, float(value)))
    except (TypeError, ValueError):
        return default


def _score(
    item: dict,
    independent_sources: int = 1,
    persistence: float = 0.0,
    purchase_intent: float = 0.0,
    competition: float = 0.5,
    safety: float = 0.5,
    testability: float = 0.5,
) -> float:
    # Higher is better except competition, production complexity, regulation,
    # logistics and inventory risk, which are inverted below.
    weights = {
        "signal": 0.12,
        "source": 0.09,
        "persistence": 0.10,
        "audience": 0.07,
        "purchase_intent": 0.12,
        "gap": 0.08,
        "competition": 0.07,
        "price_fit": 0.05,
        "margin": 0.06,
        "production": 0.03,
        "regulation": 0.04,
        "logistics": 0.02,
        "sustainability": 0.02,
        "inventory": 0.02,
        "culture": 0.02,
        "testability": 0.04,
        "safety": 0.06,
    }
    values = {
        "signal": _bounded(item.get("signal_strength")),
        "source": _bounded(independent_sources / 3),
        "persistence": _bounded(persistence),
        "audience": _bounded(item.get("audience_size")),
        "purchase_intent": _bounded(purchase_intent),
        "gap": _bounded(item.get("unmet_need")),
        "competition": 1 - _bounded(competition),
        "price_fit": _bounded(item.get("price_fit"), 0.5),
        "margin": _bounded(item.get("gross_margin_estimate"), 0.5),
        "production": 1 - _bounded(item.get("production_complexity"), 0.5),
        "regulation": 1 - _bounded(item.get("regulatory_burden"), 0.5),
        "logistics": 1 - _bounded(item.get("logistics_complexity"), 0.5),
        "sustainability": _bounded(item.get("sustainability_fit"), 0.5),
        "inventory": 1 - _bounded(item.get("inventory_risk"), 0.5),
        "culture": _bounded(item.get("cultural_fit"), 0.5),
        "testability": _bounded(testability),
        "safety": _bounded(safety),
    }
    return round(100 * sum(weights[k] * values[k] for k in weights), 2)


def build_card(
    item: dict,
    independent_sources: int | None = None,
    persistence: float = 0.0,
    purchase_intent: float = 0.0,
    competition: float = 0.5,
    safety: float = 0.5,
    testability: float = 0.5,
) -> dict:
    sources = item.get("sources") or []
    if independent_sources is None:
        independent_sources = int(item.get("independent_sources", len(sources) or 1))
    independent_sources = max(0, int(independent_sources))

    primary = {
        "source": item.get("source"),
        "url": item.get("url"),
        "observed_at": item.get("observed_at"),
    }
    evidence = [primary] + [
        s for s in sources
        if isinstance(s, dict) and s.get("url") and s.get("url") != primary.get("url")
    ]
    evidence = evidence[:20]

    score = _score(
        item, independent_sources, persistence, purchase_intent,
        competition, safety, testability,
    )
    return {
        "schema": "IMA-TREND-TO-BRAND-CARD-1.1",
        "id": digest(json.dumps(item, sort_keys=True)),
        "status": "RESEARCH_ONLY",
        "opportunity_score": score,
        "problem": item.get("problem"),
        "audience": item.get("audience"),
        "demand_evidence": evidence,
        "independent_sources": independent_sources,
        "evidence_state": "MULTI_SOURCE" if independent_sources >= 2 else "SINGLE_SOURCE_PENDING",
        "significant_conclusion_allowed": independent_sources >= 2,
        "geography": item.get("geography"),
        "language": item.get("language"),
        "sample": item.get("sample"),
        "biases": item.get("biases", []),
        "reliability": item.get("reliability"),
        "trend_change": item.get("trend_change"),
        "uncertainty": item.get("uncertainty"),
        "facts": item.get("facts", []),
        "estimates": item.get("estimates", []),
        "hypotheses": item.get("hypotheses", []),
        "mvp": item.get("mvp"),
        "cost_range": item.get("cost_range"),
        "supplier_candidates": item.get("supplier_candidates", []),
        "regulatory_notes": item.get("regulatory_notes", []),
        "risks": item.get("risks", []),
        "cheap_experiment": item.get("cheap_experiment"),
        "success_metrics": item.get("success_metrics", []),
        "stop_conditions": item.get("stop_conditions", []),
        "next_action": (
            "collect independent public evidence and validate demand before any commerce action"
        ),
        "creator_fit": item.get("creator_fit"),
        "creator_rights_status": item.get("creator_rights_status", "UNVERIFIED"),
        "commerce_channel_status": item.get("commerce_channel_status", "UNVERIFIED"),
        "legal_basis": item.get("legal_basis"),
        "commercial_action_allowed": False,
    }


def run(discovery_items=None):
    items = discovery_items or []
    cards = [
        build_card(item)
        for item in items[:100]
        if isinstance(item, dict) and item.get("url")
    ]
    state = {
        "schema": "IMA-TREND-TO-BRAND-1.1",
        "timestamp": now(),
        "candidate_count": len(cards),
        "cards": cards,
        "policy": {
            "public_sources_only": True,
            "independent_evidence_required": True,
            "no_private_data": True,
            "no_impersonation": True,
            "no_spam": True,
            "no_purchase_or_publication": True,
            "human_approval_for_commerce": True,
            "facts_estimates_hypotheses_separated": True,
            "platform_availability_must_be_verified": True,
        },
    }
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return state
