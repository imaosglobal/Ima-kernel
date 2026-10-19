#!/usr/bin/env python3
"""Evidence-only monetization readiness audit for the single IMA Global Health Loop."""
from __future__ import annotations
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def load(path): return json.loads((ROOT / path).read_text(encoding="utf-8"))
def main():
    revenue = load("docs/IMA_CREATOR_REVENUE_REGISTRY.json")
    return {
        "schema":"IMA-MONETIZATION-READINESS-1.1",
        "status":"READY_FOR_HUMAN_AUTHORIZATION",
        "primary_payment_provider":"paypal",
        "blockers":["PAYPAL_LIVE_ACCOUNT_NOT_VERIFIED"],
        "findings":[{
            "route":"PayPal",
            "status":"HUMAN_ACTIVATION_REQUIRED",
            "reason":"PayPal provides official Israeli business/payment services, but repository evidence cannot prove that a live account, bank link, compliance approval and payout permission are active."
        },{
            "route":"Revenue ledger",
            "status":"READY_FOR_EVIDENCE",
            "principle":revenue.get("monetization",{}).get("principle"),
            "rule":"views/followers/eligibility/estimates/projections are never income"
        }],
        "actual_revenue":0,
        "actual_revenue_claimed":False,
        "autonomous_spending":False,
        "next_actions":["activate and verify PayPal Business","link authorized bank and complete compliance","enable appropriate PayPal checkout/payment-link/payment-request route","store API credentials only in deployment secrets","verify a human-authorized real transaction if appropriate","record actual payout evidence","verify YouTube and GitHub Sponsors separately"]
    }
if __name__ == "__main__": print(json.dumps(main(),ensure_ascii=False,indent=2))
