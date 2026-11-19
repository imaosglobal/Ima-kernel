import os
import requests

def ask(prompt):
    api_key = os.getenv("XAI_API_KEY")
    if not api_key:
        return "[xai connector: no API key]"
    response = requests.post(
        "https://api.x.ai/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": os.getenv("XAI_MODEL", "grok-4"),
            "messages": [{"role": "user", "content": prompt}]
        },
        timeout=45,
    )
    data = response.json()
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        return f"[xai error: {data}]"
