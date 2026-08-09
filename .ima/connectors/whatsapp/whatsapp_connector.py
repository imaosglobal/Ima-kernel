from memory.user_memory import remember_user, recall_user

class Whatsapp:
    def receive_message(self, user_id, msg):
        mem = recall_user(user_id)
        history = mem.get("history", [])
        
        # בונים תשובה קצרה לפי ההיסטוריה
        if len(history) > 1:
            reply = f"כן אני זוכרת. דיברנו כבר {len(history)//2} פעמים. אתה בסדר?"
        else:
            reply = "אני איתך. מה עובר עליך עכשיו?"
            
        remember_user(user_id, "last_message", msg)
        remember_user(user_id, "last_response", reply)
        return reply
    
    def send_message(self, user_id, text):
        print(f"SEND TO {user_id}: {text}")

whatsapp = Whatsapp()
