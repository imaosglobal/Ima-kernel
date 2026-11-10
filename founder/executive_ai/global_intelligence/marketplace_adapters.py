"""Generic marketplace and intelligence routing layer for IMA.

Adapters describe how an opportunity can be monetized or which intelligence
provider can execute/reason about it. They do not bypass logins, platform
rules, consent, spending controls, or seller/buyer authorization.
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
    Marketplace("Affiracle", "affiliate_network", "Israel/global", "commission", "affiliate_link", "https://affiracle.com/"),
    Marketplace("Facebook Marketplace", "commerce", "country-dependent", "sale_margin_or_referral", "seller_or_buyer_handoff", "https://www.facebook.com/marketplace/"),
    Marketplace("eBay", "commerce", "global", "commission", "partner_program", "https://www.ebay.com/"),
    Marketplace("Amazon", "commerce", "country-dependent", "commission", "partner_program", "https://www.amazon.com/"),
    Marketplace("impact.com", "partnerships", "global", "commission_or_referral", "partner_dashboard_or_api", "https://impact.com/"),
)


@dataclass(frozen=True)
class IntelligenceProvider:
    name: str
    kind: str
    endpoint: str
    auth_env: str
    models: tuple[str, ...]
    capabilities: tuple[str, ...] = ()


INTELLIGENCE_PROVIDERS = (
    IntelligenceProvider(
        "Meta Muse",
        "agentic_model_api",
        "https://api.meta.ai/v1",
        "MODEL_API_KEY",
        ("muse-spark-1.3", "muse-wonder-1.0", "muse-ember-1.0"),
        ("responses", "tool_calling", "structured_output", "search_grounding", "multimodal"),
    ),
    IntelligenceProvider(
        "Meta Muse Spark Open",
        "open_weight_model",
        "self_hosted",
        "",
        ("muse-spark-open",),
        ("multimodal", "agentic", "self_hosted"),
    ),
)


def all_marketplaces():
    return [m.__dict__.copy() for m in MARKETPLACES]


def all_intelligence_providers():
    return [p.__dict__.copy() for p in INTELLIGENCE_PROVIDERS]


def route_for(deal: dict) -> list[dict]:
    category = str(deal.get("category", "")).lower()
    source = str(deal.get("source", "")).lower()
    routes = []
    for m in MARKETPLACES:
        if m.name == "Affiracle" and (
            source == "affiracle"
            or (source in {"aliexpress", "aliexpress network"} and category in {"general", "equipment", "software", "vehicles", "food"})
        ):
            route = m.__dict__.copy()
            route["campaign"] = "AliExpress Network"
            route["tracking_link"] = "https://track.affiracle.com/l/QQPocpwVfuYfpR3HLtAnHt"
            route["attribution_required"] = True
            routes.append(route)
        elif m.name == "impact.com" and category in {"services", "b2b", "software", "insurance", "travel", "real_estate"}:
            routes.append(m.__dict__.copy())
        elif m.name in {"Facebook Marketplace", "eBay"} and category in {"vehicles", "equipment", "food", "services"}:
            routes.append(m.__dict__.copy())
        elif m.name in {"AliExpress", "Amazon"} and category in {"equipment", "food", "software", "vehicles"}:
            routes.append(m.__dict__.copy())
        elif m.name == "PayPal" and deal.get("payout_amount"):
            routes.append(m.__dict__.copy())
    return routes


def route_intelligence(task: dict) -> list[dict]:
    """Return providers with an explicit billing-safe execution state.

    Meta 402/billing_not_configured is a hard stop for live API execution until
    billing is intentionally enabled. IMA must not retry a paid provider
    automatically or imply that planning readiness means live availability.
    """
    import os

    requested = str(task.get("provider", "")).lower()
    providers = []
    for provider in INTELLIGENCE_PROVIDERS:
        if requested and requested not in {provider.name.lower(), "meta", "muse"}:
            continue
        item = provider.__dict__.copy()
        configured = bool(os.environ.get(provider.auth_env)) if provider.auth_env else False
        item["configured"] = configured

        if provider.name == "Meta Muse":
            item["billing_policy"] = "disabled_until_explicit_billing"
            item["live_api_allowed"] = False
            item["status"] = "billing_blocked" if configured else "not_configured"
            item["retry_on_402"] = False
            item["fallback_required"] = True
        elif provider.name == "Meta Muse Spark Open":
            item["live_api_allowed"] = False
            item["status"] = "documented_only"
            item["hardware_gate"] = "not_activated_on_current_mobile_environment"
        else:
            item["status"] = "ready" if configured else "not_configured"
            item["live_api_allowed"] = configured
        providers.append(item)
    return providers


def ali_express_affiliate_plan(product_query: str) -> dict:
    """Create a non-purchasing handoff plan: intelligence researches, IMA attributes."""
    route = route_for({"source": "affiracle", "category": "general"})[0]
    return {
        "provider": "Meta Muse",
        "task": "research_and_compare",
        "query": product_query,
        "commerce_source": "AliExpress",
        "affiliate_network": "Affiracle",
        "tracking_link": route["tracking_link"],
        "purchase_mode": "human_approval_required",
        "disclosure_required": True,
        "attribution_required": True,
    }
