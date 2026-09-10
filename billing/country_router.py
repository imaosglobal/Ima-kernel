from billing.router import available


COUNTRY_RULES = {
    "IL": {
        "currency": "ILS",
        "preferred": ["payplus", "cardcom", "pelecard"],
    },
    "US": {
        "currency": "USD",
        "preferred": ["adyen", "checkout_com", "braintree"],
    },
    "GB": {
        "currency": "GBP",
        "preferred": ["adyen", "checkout_com"],
    },
    "EU": {
        "currency": "EUR",
        "preferred": ["adyen", "checkout_com", "mollie"],
    },
}


def route_payment(platform, country, currency=None, capability="cards"):
    country = country.upper()

    # Android digital subscriptions are handled by Google Play.
    if platform == "android" and capability in (
        "subscription",
        "subscriptions",
    ):
        matches = available(
            platform="android",
            capability="subscriptions",
            provider_type="platform",
        )
        if matches:
            return matches[0]

    rule = COUNTRY_RULES.get(country)

    if not rule:
        rule = {
            "currency": currency,
            "preferred": [],
        }

    if currency is None:
        currency = rule.get("currency")

    candidates = available(
        platform=platform,
        capability="cards",
        provider_type="psp",
    )

    # Never automatically select Tranzila.
    candidates = [
        provider
        for provider in candidates
        if provider["id"] != "tranzila"
    ]

    for provider_id in rule.get("preferred", []):
        for provider in candidates:
            if provider["id"] == provider_id:
                return provider

    if candidates:
        return candidates[0]

    raise RuntimeError(
        f"No configured billing provider for "
        f"platform={platform}, country={country}, "
        f"currency={currency}, capability={capability}"
    )
