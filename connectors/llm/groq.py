import os
import requests

def ask(prompt):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "[groq connector: no API key]"

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openai/gpt-oss-120b",
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    data = response.json()
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        return f"[groq error: {data}]"
