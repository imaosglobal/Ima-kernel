from billing.core import payment_plan
from billing.store import billing_store


def create_customer(user_id, email, country, currency, platform):
    plan = payment_plan(
        platform=platform,
        country=country,
        currency=currency,
        product={"id": "ima_pro", "capability": "cards"},
    )

    data = {
        "user_id": user_id,
        "email": email,
        "country": country.upper(),
        "currency": currency,
        "provider": plan["provider"],
    }

    return billing_store.create_customer(data)


def create_subscription(
    user_id,
    product_id,
    amount,
    currency,
    country,
    platform,
):
    plan = payment_plan(
        platform=platform,
        country=country,
        currency=currency,
        product={
            "id": product_id,
            "capability": "subscription",
        },
    )

    data = {
        "user_id": user_id,
        "provider": plan["provider"],
        "product_id": product_id,
        "status": "pending",
        "currency": currency,
        "amount": amount,
    }

    return billing_store.create_subscription(data)
