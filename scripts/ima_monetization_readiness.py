#!/usr/bin/env python3
"""Evidence-only monetization readiness audit for the single IMA Global Health Loop.

This audit never spends money, enrolls in programs, signs agreements, publishes paid
ads, or treats estimates as revenue. It reports what is actually evidenced in the repo.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def main():
    revenue = load("docs/IMA_CREATOR_REVENUE_REGISTRY.json")
    publication = load("docs/IMA_CREATOR_PUBLICATION_REGISTRY.json")
    commerce = load("founder/data/commerce_pipeline.json")
    monetization = load("kernel/core/monetization.json")

    findings = []
    blockers = []

    # Provider/payment evidence
    stripe_live = False  # live payment credentials/status are intentionally not stored in git
    if not stripe_live:
        blockers.append("STRIPE_LIVE_NOT_VERIFIED")
        findings.append({"route":"Stripe","status":"BLOCKED","reason":"repository contains no live payment verification; sandbox/live state must be verified outside source control"})

    # Creator revenue routes
    for item in revenue.get("distribution", {}).get("verified_destinations", []):
        findings.append({
            "route": item.get("platform"),
            "status": "WRITE_VERIFIED" if item.get("write_verified") else "WRITE_NOT_VERIFIED",
            "account": item.get("account_id"),
        })

    pub_status = publication.get("status")
    if pub_status != "published_verified":
        blockers.append("CREATOR_PUBLICATION_NOT_VERIFIED")
        findings.append({"route":"Creator publication","status":"BLOCKED","reason":pub_status})

    if not commerce:
        blockers.append("COMMERCE_PIPELINE_EMPTY")
        findings.append({"route":"Creator-to-Commerce","status":"BLOCKED","reason":"no verified commerce opportunity has reached the pipeline"})

    # Existing package-level monetization is explicitly future-only.
    if monetization.get("premium") is False and monetization.get("donations") is False:
        blockers.append("NO_NATIVE_PAYMENT_FEATURE")
        findings.append({"route":"IMA native checkout","status":"BLOCKED","reason":"kernel monetization config currently disables donations and premium"})

    # Revenue truth
    findings.append({
        "route":"Revenue ledger",
        "status":"READY_FOR_EVIDENCE",
        "principle": revenue.get("monetization", {}).get("principle"),
        "rule":"views/followers/eligibility/estimates/projections are never income",
    })

    result = {
        "schema":"IMA-MONETIZATION-READINESS-1.0",
        "status":"READY_FOR_HUMAN_AUTHORIZATION" if blockers else "VERIFIED_ROUTE_AVAILABLE",
        "blockers":blockers,
        "findings":findings,
        "actual_revenue":0,
        "actual_revenue_claimed":False,
        "autonomous_spending":False,
        "next_actions":[
            "verify one live, legally available payout route with the account owner",
            "record platform eligibility/enrollment evidence",
            "publish only after write permission and content eligibility are verified",
            "record actual payout evidence in the canonical revenue ledger",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
