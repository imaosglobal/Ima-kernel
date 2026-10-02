"""IMA Outcome Engine: outcome-as-a-service pipeline inspired by proven publisher/operator models.

The engine evaluates opportunities before scale, assembles the smallest useful
execution plan, and keeps external actions proof/consent-gated. IMA sells and
measures outcomes rather than pretending that one model or one agent is the
product.
"""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

ROOT = Path("founder/data")
OUTPUT = ROOT / "ima_outcome_pipeline.json"

STAGES = (
    "DISCOVER",
    "PMF_TEST",
    "VALIDATE",
    "BUILD",
    "GROW",
    "RETAIN",
    "OUTCOME",
)

SERVICES = (
    "product_positioning",
    "store_or_landing_page",
    "creative_and_content",
    "search_and_ai_discovery",
    "paid_media_planning",
    "conversion_experiments",
    "analytics_and_data",
    "customer_retention",
    "affiliate_and_referral_routing",
    "commerce_operations",
)

def _load(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default
    except Exception:
        return default

def _text(row):
    return " ".join(str(row.get(k, "")) for k in ("title", "signal", "description", "need", "category")).lower()

def _score(row):
    text = _text(row)
    score = 0
    evidence = []

    demand_terms = ("need", "needed", "looking for", "seeking", "buyer", "supplier", "rfp", "purchase")
    product_terms = ("product", "brand", "software", "service", "saas", "food", "health", "consumer", "commerce")
    growth_terms = ("global", "worldwide", "market", "subscription", "recurring", "commission", "referral", "sales")
    proof_terms = ("patent", "study", "research", "validated", "revenue", "customers", "evidence")

    if any(t in text for t in demand_terms):
        score += 30
        evidence.append("demand signal")
    if any(t in text for t in product_terms):
        score += 20
        evidence.append("product/service fit")
    if any(t in text for t in growth_terms):
        score += 20
        evidence.append("distribution or monetization signal")
    if any(t in text for t in proof_terms):
        score += 20
        evidence.append("proof signal")
    if row.get("payout_amount") is not None or row.get("payout_model"):
        score += 10
        evidence.append("commercial route")

    return min(100, score), evidence

def build_candidate(row, source_kind):
    score, evidence = _score(row)
    raw = f"{source_kind}|{row.get('id','')}|{row.get('url','')}|{row.get('title','')}"
    candidate_id = hashlib.sha256(raw.encode()).hexdigest()[:20]

    if score >= 75:
        stage = "VALIDATE"
    elif score >= 50:
        stage = "PMF_TEST"
    else:
        stage = "DISCOVER"

    return {
        "candidate_id": candidate_id,
        "source_kind": source_kind,
        "title": str(row.get("title") or row.get("need") or "IMA opportunity")[:300],
        "category": row.get("category", "general"),
        "url": row.get("url"),
        "score": score,
        "evidence": evidence,
        "stage": stage,
        "services": list(SERVICES),
        "execution_policy": "proof-gated",
        "external_contact": "disabled_until_explicit_consent",
        "purchase_or_spend": "disabled_until_explicit_authorization",
        "partner_ip": "retained_by_partner",
        "commercial_model": "outcome_or_success_based_where_supported",
        "created_at": time.time(),
    }

def run():
    demand = _load(ROOT / "public_demand_signals.json", [])
    deals = _load(ROOT / "deal_hunter_opportunities.json", [])
    graph = _load(ROOT / "global_opportunity_graph.json", [])

    rows = []
    for row in demand[:500]:
        rows.append(build_candidate(row, "demand"))
    for row in deals[:500]:
        rows.append(build_candidate(row, "deal"))
    if isinstance(graph, list):
        for row in graph[:500]:
            rows.append(build_candidate(row, "opportunity_graph"))

    unique = {}
    for row in rows:
        unique[row["candidate_id"]] = row

    pipeline = sorted(
        unique.values(),
        key=lambda x: (x["score"], x["created_at"]),
        reverse=True,
    )[:1000]

    state = {
        "schema": "IMA-OUTCOME-AS-A-SERVICE-1.0",
        "positioning": "IMA operates as an outcome partner: people and agents where useful, shared data and tooling where useful, verified results as the product.",
        "stages": list(STAGES),
        "services": list(SERVICES),
        "commercial_principles": {
            "ip": "partner-retained",
            "pricing": "outcome_or_success_based_where_supported",
            "proof": "required_before_claiming_success",
            "consent": "required_before_external_contact",
            "spend": "requires_explicit_authorization",
        },
        "candidate_count": len(pipeline),
        "candidates": pipeline,
        "updated_at": time.time(),
    }
    ROOT.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return state

if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
