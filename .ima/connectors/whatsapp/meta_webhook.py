import os
import sys
from pathlib import Path

from flask import Flask, request

# ------------------------------------------------------------
# CANONICAL IMA WhatsApp Webhook
#
# Flow:
# WhatsApp -> receive_message -> stream.emit -> memory
#         -> response -> send_message -> stream.emit -> memory
#
# No second memory.
# No second event bus.
# No duplicate receive/send events.
# ------------------------------------------------------------

CURRENT = Path(__file__).resolve().parents[2]
RUNTIME = CURRENT / ".ima" / "runtime"

if str(CURRENT) not in sys.path:
    sys.path.insert(0, str(CURRENT))

if str(RUNTIME) not in sys.path:
    sys.path.insert(0, str(RUNTIME))

from connectors.whatsapp.whatsapp_connector import whatsapp


app = Flask(__name__)

VERIFY_TOKEN = os.getenv(
    "META_VERIFY_TOKEN",
    "ima_verify_token"
)


def generate_response(user_id, message):
    """
    Temporary deterministic response layer.

    This is deliberately separate from the event/memory layer.
    The real IMA/LLM response engine can replace this function
    without changing the WhatsApp event architecture.
    """
    return "קיבלתי וזכרתי"


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
        data = request.get_json(silent=True) or {}

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

                    # ONE canonical input event.
                    whatsapp.receive_message(
                        user_id,
                        text
                    )

                    # Response generation is separate from transport.
                    reply = generate_response(
                        user_id,
                        text
                    )

                    # ONE canonical output event.
                    whatsapp.send_message(
                        user_id,
                        reply
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
