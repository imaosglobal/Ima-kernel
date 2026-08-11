import os, time, json, requests
from dotenv import load_dotenv
load_dotenv()

class WhatsAppSender:
    def __init__(self, token, phone_id):
        self.token = token
        self.phone_id = phone_id
    def send_message(self, to, text):
        url = f"https://graph.facebook.com/v20.0/{self.phone_id}/messages"
        headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        data = {"messaging_product": "whatsapp", "to": to, "type": "text", "text": {"body": text}}
        try: return requests.post(url, headers=headers, json=data, timeout=20).json()
        except Exception as e: return {"error": str(e)}

sender = WhatsAppSender(os.getenv("WA_TOKEN"), os.getenv("WA_PHONE_ID"))
report_to = os.getenv("WA_REPORT_TO")

print(f"אמא עלתה. שולחת בדיקה ל-{report_to}")
sender.send_message(report_to, "אמא מחוברת ✅ הכספת מלאה")

print("כדי שאמא תענה אוטומטית צריך Webhook. בינתיים נבדוק ידנית")
