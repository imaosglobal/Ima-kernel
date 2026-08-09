import requests
import json

URL = "http://127.0.0.1:8000/chat"
print("=== IMA CHAT ===")
print("כתוב exit ליציאה\n")

while True:
    user_input = input("אתה: ")
    if user_input.lower() == "exit":
        break
    
    try:
        res = requests.post(URL, json={"text": user_input})
        print(res.text)  # נדפיס את כל מה שהשרת מחזיר
    except Exception as e:
        print(f"שגיאה: {e}")

print("ביי אורי 💛")
