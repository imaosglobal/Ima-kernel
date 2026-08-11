import os
import requests

def ask(prompt):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "[gemini connector: no API key]"

    response = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}",
        headers={"content-type": "application/json"},
        json={"contents": [{"parts": [{"text": prompt}]}]}
    )
    data = response.json()
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        return f"[gemini error: {data}]"
