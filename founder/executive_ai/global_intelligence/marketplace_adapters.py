"""Generic marketplace routing layer for IMA Deal Hunter.

Adapters describe how an opportunity can be monetized; they do not bypass
logins, platform rules, consent, or seller/buyer authorization.
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Marketplace:
    name: str
    kind: str
    regions: str
    payout_model: str
    submit_mode: str
    url: str

MARKETPLACES = (
    Marketplace("PayPal", "payments", "global", "payment", "api_or_account", "https://www.paypal.com/"),
    Marketplace("AliExpress", "commerce", "global", "commission", "partner_program", "https://www.aliexpress.com/"),
    Marketplace("Facebook Marketplace", "commerce", "country-dependent", "sale_margin_or_referral", "seller_or_buyer_handoff", "https://www.facebook.com/marketplace/"),
    Marketplace("eBay", "commerce", "global", "commission", "partner_program", "https://www.ebay.com/"),
    Marketplace("Amazon", "commerce", "country-dependent", "commission", "partner_program", "https://www.amazon.com/"),
    Marketplace("impact.com", "partnerships", "global", "commission_or_referral", "partner_dashboard_or_api", "https://impact.com/"),
)

def all_marketplaces():
    return [m.__dict__.copy() for m in MARKETPLACES]

def route_for(deal: dict) -> list[dict]:
    category = str(deal.get("category", "")).lower()
    routes = []
    for m in MARKETPLACES:
        if m.name == "impact.com" and category in {"services", "b2b", "software", "insurance", "travel", "real_estate"}:
            routes.append(m.__dict__.copy())
        elif m.name in {"Facebook Marketplace", "eBay"} and category in {"vehicles", "equipment", "food", "services"}:
            routes.append(m.__dict__.copy())
        elif m.name in {"AliExpress", "Amazon"} and category in {"equipment", "food", "software", "vehicles"}:
            routes.append(m.__dict__.copy())
        elif m.name == "PayPal" and deal.get("payout_amount"):
            routes.append(m.__dict__.copy())
    return routes
