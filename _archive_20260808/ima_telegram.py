import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TOKEN = "שים_כאן_את_הטוקן_שלך_מ_BotFather"
API_URL = "http://localhost:5000/ima"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    sender = update.message.from_user.first_name
    r = requests.post(API_URL, json={"text": text, "sender": sender})
    await update.message.reply_text(r.json()["reply"])

app = Application.builder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
print("בוט טלגרם עלה")
app.run_polling()
