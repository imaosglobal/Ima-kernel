import os
import requests

def ask(prompt):
    api_key = os.getenv("CLAUDE_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return "[anthropic connector: no API key]"

    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        },
        json={
            "model": "claude-sonnet-4-5",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    data = response.json()
    if "content" in data:
        return data["content"][0]["text"]
    return f"[anthropic error: {data}]"
