import os
import sys

from flask import Flask, request

ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../..")
)

if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from connectors.whatsapp.whatsapp_connector import whatsapp

app = Flask(__name__)

VERIFY_TOKEN = os.getenv(
    "META_VERIFY_TOKEN",
    "ima_verify_token"
)


@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200

    return "verification failed", 403


@app.route("/webhook", methods=["POST"])
def receive():
    try:
        data = request.json or {}

        for item in data.get("entry", []):
            for change in item.get("changes", []):
                value = change.get("value", {})

                for msg in value.get("messages", []):
                    user_id = msg.get("from")

                    text = ""
                    if "text" in msg:
                        text = msg["text"].get("body", "")

                    if not user_id or not text:
                        continue

                    # Canonical inbound event.
                    # receive_message() owns event emission.
                    whatsapp.receive_message(
                        user_id,
                        text
                    )

        return "OK", 200

    except Exception as e:
        print("WEBHOOK ERROR:", e)
        return "ERROR", 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))

    app.run(
        host="0.0.0.0",
        port=port
    )
