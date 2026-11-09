[Reading 38 lines from start (total: 38 lines, 0 remaining)]

import json
import os
import urllib.request

API = "https://api.openai.com/v1/responses"

def ask(prompt):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "[openai connector: no API key]"
    model = os.getenv("OPENAI_MODEL", "gpt-6-luna")
    payload = {
        "model": model,
        "input": [{"role": "user", "content": prompt}],
    }
    req = urllib.request.Request(
        API,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": "Bearer " + api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=45) as response:
            data = json.loads(response.read().decode("utf-8"))
        text = data.get("output_text")
        if text:
            return text
        for item in data.get("output", []):
            for content in item.get("content", []):
                if content.get("type") in {"output_text", "text"} and content.get("text"):
                    return content["text"]
        return "[openai error: empty response]"
    except Exception as exc:
        return "[openai error: " + type(exc).__name__ + "]"

[executed on device: localhost (863839ba-718b-4553-b9ea-247cfb8980b8)]