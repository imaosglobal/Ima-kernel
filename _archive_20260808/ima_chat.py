import requests
import json

URL = "http://127.0.0.1:8000/chat"

while True:
    user_input = input("אתה: ")
    if user_input.lower() == "exit":
        break
    
    try:
        res = requests.post(URL, json={"text": user_input})
    except Exception as e:

