import json
import os
import time
import urllib.request
from pathlib import Path

REGISTRY = Path(".ima/llm_models.json")
CACHE_TTL = 21600


def _get(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())


def discover_gemini():
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        return []
    try:
        data = _get("https://generativelanguage.googleapis.com/v1beta/models?key=" + key)
        out = []
        for m in data.get("models", []):
            name = m.get("name", "").split("models/")[-1]
            methods = m.get("supportedGenerationMethods", [])
            if name and "generateContent" in methods:
                out.append(name)
        return out
    except Exception:
        return []


def discover_openai():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        return []
    try:
        data = _get("https://api.openai.com/v1/models", {"Authorization": "Bearer " + key})
        return [x.get("id") for x in data.get("data", []) if x.get("id")]
    except Exception:
        return []


def discover_anthropic():
    key = os.getenv("ANTHROPIC_API_KEY") or os.getenv("CLAUDE_API_KEY")
    if not key:
        return []
    try:
        data = _get("https://api.anthropic.com/v1/models", {
            "x-api-key": key, "anthropic-version": "2023-06-01"
        })
        return [x.get("id") for x in data.get("data", []) if x.get("id")]
    except Exception:
        return []


def _stable_choice(provider, models):
    models = [m for m in models if m]
    if provider == "gemini":
        preferred = ["gemini-3.8-flash", "gemini-3.7-flash", "gemini-3.6-flash", "gemini-3.5-flash"]
    elif provider == "openai":
        preferred = ["gpt-5.6", "gpt-5.6-luna", "gpt-5.6-terra", "gpt-5.6-sol"]
    else:
        preferred = ["claude-sonnet-4-5", "claude-sonnet-4-0"]
    for wanted in preferred:
        if wanted in models:
            return wanted
    return models[0] if models else None


def refresh(force=False):
    if not force and REGISTRY.exists():
        try:
            data = json.loads(REGISTRY.read_text(encoding="utf8"))
            if time.time() - data.get("time", 0) < CACHE_TTL:
                return data
        except Exception:
            pass
    data = {"time": time.time(), "providers": {}}
    for provider, fn in (("gemini", discover_gemini), ("openai", discover_openai), ("anthropic", discover_anthropic)):
        models = fn()
        data["providers"][provider] = {"models": models, "selected": _stable_choice(provider, models)}
    REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf8")
    return data


def recommended(provider=None):
    data = refresh()
    if provider:
        return data.get("providers", {}).get(provider, {}).get("selected")
    for name in ("openai", "anthropic", "gemini"):
        value = data.get("providers", {}).get(name, {}).get("selected")
        if value:
            return name, value
    return None, None


# Safe periodic code scan: syntax validation only; never rewrites source files.
def _scan_code(root=Path(".")):
    import py_compile
    checked = 0
    errors = []
    for path in root.rglob("*.py"):
        if any(part in {".git", "node_modules", "__pycache__"} for part in path.parts):
            continue
        try:
            py_compile.compile(str(path), doraise=True)
            checked += 1
        except Exception as e:
            errors.append({"file": str(path), "error": str(e)})
    return {"checked": checked, "errors": errors}

_original_refresh = refresh

def refresh(force=False):
    data = _original_refresh(force)
    if force or "code_scan" not in data:
        data["code_scan"] = _scan_code()
        REGISTRY.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf8")
    return data
