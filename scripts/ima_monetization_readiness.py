#!/usr/bin/env python3
"""Evidence-only monetization readiness audit for the single IMA Global Health Loop."""
from __future__ import annotations
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def main():
    revenue = load("docs/IMA_CREATOR_REVENUE_REGISTRY.json")
    monetization = load("kernel/core/monetization.json")
    router = monetization["payment_provider"]
    providers = [p["id"] for p in router["providers"]]
    blockers = []
    if "paypal" not in providers:
        blockers.append("PAYPAL_PROVIDER_MISSING")
    if "google_pay" not in providers:
        blockers.append("GOOGLE_PAY_PROVIDER_MISSING")
    if "apple_pay" not in providers:
        blockers.append("APPLE_PAY_PROVIDER_MISSING")
    if router.get("credentials_location") != "runtime_secret_store_only":
        blockers.append("CREDENTIALS_LOCATION_INVALID")
    if not router.get("credentials_must_not_be_committed", False):
        blockers.append("CREDENTIAL_COMMIT_POLICY_MISSING")
    return {
        "schema": "IMA-MONETIZATION-READINESS-1.2",
        "status": "READY_FOR_HUMAN_AUTHORIZATION" if not blockers else "BLOCKED",
        "payment_router_mode": router["mode"],
        "primary_payment_provider": router["primary"],
        "providers": providers,
        "blockers": blockers,
        "findings": [
            {
                "route": "Multi-provider payment router",
                "status": "HUMAN_ACTIVATION_REQUIRED",
                "reason": "Provider configuration in the repository does not prove live merchant activation, eligibility, compliance approval or payout permission."
            },
            {
                "route": "Revenue ledger",
                "status": "READY_FOR_EVIDENCE",
                "principle": revenue.get("monetization", {}).get("principle"),
                "rule": "views/followers/eligibility/estimates/projections are never income"
            }
        ],
        "actual_revenue": 0,
        "actual_revenue_claimed": False,
        "autonomous_spending": False,
        "next_actions": [
            "activate and verify each desired provider externally",
            "complete required merchant/business, bank, compliance and payout setup",
            "store API credentials only in deployment/runtime secrets",
            "verify a human-authorized real transaction if appropriate",
            "record actual receipt/payout evidence",
            "verify YouTube and GitHub Sponsors separately"
        ]
    }

if __name__ == "__main__":
    print(json.dumps(main(), ensure_ascii=False, indent=2))
