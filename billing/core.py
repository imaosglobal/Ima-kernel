from billing.country_router import route_payment


def select_provider(
    platform,
    country,
    currency=None,
    capability="cards",
):
    return route_payment(
        platform=platform,
        country=country,
        currency=currency,
        capability=capability,
    )


def payment_plan(
    platform,
    country,
    currency,
    product,
):
    provider = select_provider(
        platform=platform,
        country=country,
        currency=currency,
        capability=product.get("capability", "cards"),
    )

    return {
        "provider": provider["id"],
        "provider_type": provider["type"],
        "platform": platform,
        "country": country.upper(),
        "currency": currency,
        "product": product,
    }
