from flask import Blueprint, request, jsonify

from billing.core import payment_plan
from billing.adapters import get_adapter


billing_api = Blueprint(
    "billing_api",
    __name__,
    url_prefix="/billing",
)


@billing_api.post("/checkout")
def checkout():
    data = request.get_json(silent=True) or {}

    required = [
        "platform",
        "country",
        "currency",
        "product_id",
        "amount",
    ]

    missing = [x for x in required if not data.get(x)]

    if missing:
        return jsonify({
            "ok": False,
            "error": "missing_fields",
            "fields": missing,
        }), 400

    plan = payment_plan(
        platform=data["platform"],
        country=data["country"],
        currency=data["currency"],
        product={
            "id": data["product_id"],
            "capability": data.get("capability", "cards"),
        },
    )

    adapter = get_adapter(plan["provider"])

    customer = {
        "user_id": data.get("user_id", "anonymous"),
        "email": data.get("email"),
    }

    product = {
        "id": data["product_id"],
        "amount": data["amount"],
        "currency": data["currency"],
    }

    try:
        checkout_data = adapter.create_checkout(
            customer,
            product,
        )
    except NotImplementedError as exc:
        return jsonify({
            "ok": False,
            "error": "provider_not_configured",
            "provider": plan["provider"],
            "message": str(exc),
        }), 501

    return jsonify({
        "ok": True,
        "checkout": checkout_data,
    })
