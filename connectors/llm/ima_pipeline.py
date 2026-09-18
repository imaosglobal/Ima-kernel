from .model_selector import current
from .router import available_providers
from .executor import execute
from .identity_guard import wrap_response


def ask(message):
    selection = current()
    preferred = selection.get("provider")
    available = available_providers()
    order = [preferred] + [x for x in ("openai", "anthropic", "gemini", "ollama") if x != preferred]
    failures = []
    for provider in order:
        if not provider or provider not in available:
            continue
        model = selection.get("model") if provider == preferred else None
        result = execute(model=model, prompt=message, provider=provider)
        if result.get("status") == "ok" and result.get("response"):
            result["attempted_providers"] = len(failures) + 1
            return wrap_response(result, "IMA")
        failures.append({
            "provider": provider,
            "model": result.get("model"),
            "status": result.get("status"),
            "error": result.get("error"),
        })
    return wrap_response({"status":"error","response":"","attempted":failures}, "IMA")
