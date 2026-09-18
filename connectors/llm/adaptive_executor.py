import json
import os
import time
import urllib.error
import urllib.request
from .model_registry import recommended


def _request(url, payload, headers, timeout=60, retries=2):
    raw = json.dumps(payload).encode()
    last = None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, data=raw, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            last = e
            if e.code not in (429, 500, 502, 503, 504) or attempt >= retries:
                try:
                    detail = e.read().decode("utf8", "replace")[:1000]
                except Exception:
                    detail = str(e)
                raise RuntimeError(f"HTTP {e.code}: {detail}")
            time.sleep(2 ** attempt)
    raise last


def _gemini(model, prompt):
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY missing")
    model = model or recommended("gemini") or os.getenv("IMA_GEMINI_MODEL", "gemini-3.8-flash")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
    data = _request(url, {"contents":[{"parts":[{"text":prompt}]}]}, {"Content-Type":"application/json"})
    return data["candidates"][0]["content"]["parts"][0]["text"], model


def _openai(model, prompt):
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY missing")
    model = model or recommended("openai") or os.getenv("IMA_OPENAI_MODEL", "gpt-5.6")
    data = _request("https://api.openai.com/v1/chat/completions", {"model":model,"messages":[{"role":"user","content":prompt}]}, {"Content-Type":"application/json","Authorization":f"Bearer {key}"})
    return data["choices"][0]["message"]["content"], model


def _anthropic(model, prompt):
    key = os.getenv("ANTHROPIC_API_KEY") or os.getenv("CLAUDE_API_KEY")
    if not key:
        raise RuntimeError("ANTHROPIC_API_KEY missing")
    model = model or recommended("anthropic") or os.getenv("IMA_ANTHROPIC_MODEL", "claude-sonnet-4-5")
    data = _request("https://api.anthropic.com/v1/messages", {"model":model,"max_tokens":2048,"messages":[{"role":"user","content":prompt}]}, {"Content-Type":"application/json","x-api-key":key,"anthropic-version":"2023-06-01"})
    return data["content"][0]["text"], model


def _ollama(model, prompt):
    if not model:
        raise RuntimeError("Ollama model missing")
    data = _request("http://127.0.0.1:11434/api/generate", {"model":model,"prompt":prompt,"stream":False}, {"Content-Type":"application/json"}, timeout=40, retries=0)
    return data.get("response", ""), model


HANDLERS = {"gemini": _gemini, "openai": _openai, "anthropic": _anthropic, "ollama": _ollama}


def execute(model, prompt, provider=None):
    started = time.time()
    if provider not in HANDLERS:
        return {"provider":provider,"model":model,"response":"","status":"error","error":"unsupported provider","latency":time.time()-started}
    try:
        response, used_model = HANDLERS[provider](model, prompt)
        return {"provider":provider,"model":used_model,"response":response,"status":"ok","time":time.time(),"latency":time.time()-started}
    except Exception as e:
        return {"provider":provider,"model":model,"response":"","status":"error","error":str(e),"time":time.time(),"latency":time.time()-started}
