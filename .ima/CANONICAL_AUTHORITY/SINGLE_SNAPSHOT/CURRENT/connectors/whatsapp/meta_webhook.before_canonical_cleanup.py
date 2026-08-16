import os
import sys
import requests
from flask import Flask, request

sys.path.insert(0, ".")

from connectors.whatsapp.whatsapp_connector import whatsapp
from runtime.stream import emit


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
        data = request.json

        entry = data.get("entry", [])

        for item in entry:

            changes = item.get("changes", [])

            for change in changes:

                value = change.get("value", {})

                messages = value.get(
                    "messages",
                    []
                )

                for msg in messages:

                    user_id = msg.get("from")

                    text = ""

                    if "text" in msg:
                        text = msg["text"].get(
                            "body",
                            ""
                        )

                    if user_id and text:

                        emit(
                            "whatsapp_message_received",
                            user_id=user_id,
                            message=text
                        )

                        reply = whatsapp.receive_message(
                            user_id,
                            text
                        )

                        emit(
                            "whatsapp_reply_generated",
                            user_id=user_id,
                            reply=reply
                        )

                        whatsapp.send_message(
                            user_id,
                            reply
                        )

                        emit(
                            "whatsapp_reply_sent",
                            user_id=user_id
                        )

        return "OK", 200

    except Exception as e:

        print(
            "WEBHOOK ERROR:",
            e
        )

        return "ERROR", 500



if __name__ == "__main__":

    port=int(
        os.getenv(
            "PORT",
            "8000"
        )
    )

    app.run(
        host="0.0.0.0",
        port=port
    )
