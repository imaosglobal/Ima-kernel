import os
import requests
import json

from ima_master_runtime import IMA

def emit(event_type, **data):
    try:
        import importlib.util
        from pathlib import Path

        ima_root = Path(__file__).resolve().parents[5]
        stream_file = ima_root / "runtime" / "stream.py"

        spec = importlib.util.spec_from_file_location(
            "ima_runtime_stream", stream_file
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod.emit(event_type, **data)

    except Exception as e:
        print("IMA_EVENT_BRIDGE_ERROR:", e, flush=True)
        return None

        stream_file = Path(__file__).resolve().parents[4] / "runtime" / "stream.py"
        spec = importlib.util.spec_from_file_location("ima_runtime_stream", stream_file)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod.emit(event_type, **data)
    except Exception as e:
        print("IMA_EVENT_BRIDGE_ERROR:", e, flush=True)
        return None
from memory.user_memory import remember_user, recall_user

try:
    from memory.memory_answer_filter import resolve_answer
except Exception:
    resolve_answer = None


class WhatsAppConnector:

    def __init__(self):
        self.token = os.getenv("WA_TOKEN")
        self.phone_id = os.getenv("WA_PHONE_ID")


    def receive_message(self, user_id, message):
        emit("whatsapp.message_received", user_id=user_id, message=message)
        emit(
            "whatsapp.message.received",
            user_id=user_id,
            message=message
        )

        remember_user(
            user_id,
            "last_message",
            message
        )

        memory = recall_user(user_id)


        # MEMORY PREFERENCE ENGINE

        def find_text_values(obj):
            result=[]

            if isinstance(obj,dict):
                for k,v in obj.items():

                    if k=="value":
                        if isinstance(v,str):
                            result.append(v)

                    result.extend(
                        find_text_values(v)
                    )

            elif isinstance(obj,list):
                for x in obj:
                    result.extend(
                        find_text_values(x)
                    )

            return result


        if "מה אני אוהב" not in message and "אני אוהב" in message:

            value=message.split(
                "אני אוהב",
                1
            )[1].strip()

            if value:

                remember_user(
                    user_id,
                    "preference",
                    value
                )

                return (
                    "זכרתי שאתה אוהב "
                    + value
                )


        if "מה אני אוהב" in message:

            memory=recall_user(user_id)

            values=find_text_values(memory)

            values=[
                x for x in values
                if x not in [
                    "מה אני אוהב?",
                    "?",
                    ""
                ]
            ]

            if values:

                return (
                    "אני זוכרת שאתה אוהב "
                    + values[-1]
                )


        prompt = f"""
שאלה:
{message}

זיכרון נקי:
{json.dumps(memory, ensure_ascii=False)}
"""


        result = IMA.ask(prompt)


        if isinstance(result,dict):
            reply=result.get(
                "response",
                ""
            )
        else:
            reply=str(result)


        # מניעת זיהום
        bad=[
            "את IMA.",
            "זיכרון משתמש:",
            "הודעה:"
        ]

        for b in bad:
            if b in reply:
                reply=reply.split(b)[0]


        reply=reply.strip()


        remember_user(
            user_id,
            "last_response",
            reply
        )

        emit(
            "whatsapp.message.sent",
            user_id=user_id,
            response=reply
        )

        return reply



    def send_message(self, to, text):

        if not self.token or not self.phone_id:
            return {
                "status": "missing_credentials",
                "need": [
                    "WA_TOKEN",
                    "WA_PHONE_ID"
                ]
            }


        url = (
            f"https://graph.facebook.com/v20.0/"
            f"{self.phone_id}/messages"
        )


        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }


        data = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {
                "body": text
            }
        }


        try:
            r = requests.post(
                url,
                headers=headers,
                json=data,
                timeout=20
            )

            return r.json()

        except Exception as e:
            return {
                "error": str(e)
            }



whatsapp = WhatsAppConnector()
