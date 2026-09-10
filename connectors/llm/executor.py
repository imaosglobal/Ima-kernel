import json
import os
import time
import urllib.request


def _ollama(model, prompt):
    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_ctx": 2048,
            "temperature": 0.3,
        },
    }).encode()

    req = urllib.request.Request(
        "http://127.0.0.1:11434/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
    )

    with urllib.request.urlopen(req, timeout=40) as r:
        data = json.loads(r.read())

    return data.get("response", "")


def _openai(model, prompt):
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY missing")

    payload = json.dumps({
        "model": model or os.getenv(
            "IMA_OPENAI_MODEL",
            "gpt-6-astra"
        ),
        "messages": [
            {"role": "user", "content": prompt}
        ],
    }).encode()

    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}",
        },
    )

    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.loads(r.read())

    return data["choices"][0]["message"]["content"]


def _anthropic(model, prompt):
    key = (
        os.getenv("ANTHROPIC_API_KEY")
        or os.getenv("CLAUDE_API_KEY")
    )

    if not key:
        raise RuntimeError("ANTHROPIC_API_KEY missing")

    payload = json.dumps({
        "model": model or os.getenv(
            "IMA_ANTHROPIC_MODEL",
            "claude-sonnet-4-5"
        ),
        "max_tokens": 2048,
        "messages": [
            {"role": "user", "content": prompt}
        ],
    }).encode()

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
        },
    )

    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.loads(r.read())

    return data["content"][0]["text"]


def _gemini(model, prompt):
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY missing")

    model = model or os.getenv(
        "IMA_GEMINI_MODEL",
        "gemini-2.5-flash"
    )

    url = (
        "https://generativelanguage.googleapis.com/"
        f"v1beta/models/{model}:generateContent?key={key}"
    )

    payload = json.dumps({
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }).encode()

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Content-Type": "application/json"
        },
    )

    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.loads(r.read())

    return (
        data["candidates"][0]
        ["content"]["parts"][0]
        ["text"]
    )


def execute(model, prompt, provider=None):
    started = time.time()

    if provider is None:
        provider = "ollama"

    try:
        if provider == "openai":
            response = _openai(model, prompt)

        elif provider == "anthropic":
            response = _anthropic(model, prompt)

        elif provider == "gemini":
            response = _gemini(model, prompt)

        elif provider == "ollama":
            response = _ollama(model, prompt)

        else:
            raise RuntimeError(
                f"Unsupported provider: {provider}"
            )

        return {
            "provider": provider,
            "model": model,
            "response": response,
            "status": "ok",
            "time": time.time(),
            "latency": time.time() - started,
        }

    except Exception as e:
        return {
            "provider": provider,
            "model": model,
            "response": "",
            "status": "error",
            "error": str(e),
            "time": time.time(),
            "latency": time.time() - started,
        }
