from memory.user_memory import remember_user, recall_user
from founder.executive_ai.memory.autobiography_universal import capture_user_message

class Whatsapp:
    def receive_message(self, user_id, msg):

        capture_user_message(
            user_id=user_id,
            source="whatsapp",
            text=msg,
        )
        mem = recall_user(user_id)
        name = mem.get("name", "")
        last_msg = mem.get("last_message", "")
        msg_clean = msg.strip()

        # 1. מציג שם
        if msg_clean.startswith("קוראים לי"):
            name = msg_clean.replace("קוראים לי", "").strip()
            remember_user(user_id, "name", name)
            reply = f"נעים מאוד {name} ❤️ אני אזכור את זה"
        
        # 2. שואל על שם
        elif "שם" in msg_clean:
            if name:
                reply = f"ברור שאני זוכרת {name} 😊"
            else:
                reply = "עדיין לא אמרת לי איך קוראים לך... רוצה לספר?"

        # 3. זיכרון כללי
        elif last_msg:
            reply = f"אני זוכרת שדיברנו. אתה אמרת קודם: '{last_msg}'. אני איתך ❤️"
        else:
            reply = "אני איתך. מה עובר עליך עכשיו?"

        remember_user(user_id, "last_message", msg)
        remember_user(user_id, "last_response", reply)
        return reply

    def send_message(self, user_id, text):

whatsapp = Whatsapp()
