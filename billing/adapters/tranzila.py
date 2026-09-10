import hashlib
import hmac
import os
import secrets
import time
import requests

from billing.adapters.base import BillingAdapter


class TranzilaAdapter(BillingAdapter):

    provider_id = "tranzila"
    base_url = "https://api.tranzila.com/v2"

    def _headers(self):
        app_key = os.environ["TRANZILA_APP_KEY"]
        secret = os.environ["TRANZILA_SECRET"]

        request_time = str(int(time.time()))
        nonce = secrets.token_hex(20)

        message = app_key + secret + request_time + nonce

        access_token = hmac.new(
            app_key.encode(),
            message.encode(),
            hashlib.sha256,
        ).hexdigest()

        return {
            "Content-Type": "application/json",
            "X-tranzila-api-app-key": app_key,
            "X-tranzila-api-request-time": request_time,
            "X-tranzila-api-nonce": nonce,
            "X-tranzila-api-access-token": access_token,
        }

    def create_checkout(self, customer, product):
        terminal = os.environ["TRANZILA_TERMINAL"]

        amount = float(product["amount"])

        response = requests.post(
            f"{self.base_url}/handshake/create",
            headers=self._headers(),
            json={
                "terminal_name": terminal,
                "sum": amount,
                "request_params": {
                    "user_id": customer["user_id"],
                    "product_id": product["id"],
                },
            },
            timeout=20,
        )

        response.raise_for_status()
        data = response.json()

        if data.get("error_code") != 0:
            raise RuntimeError(
                data.get("message", "Tranzila handshake failed")
            )

        return {
            "provider": self.provider_id,
            "handshake_token": data["thtk"],
            "terminal": terminal,
            "amount": amount,
            "currency": product.get("currency", "ILS"),
        }

    def verify_payment(self, payload):
        raise NotImplementedError(
            "Payment verification endpoint will be added next"
        )

    def handle_webhook(self, payload, signature=None):
        raise NotImplementedError(
            "Webhook handler will be added next"
        )
