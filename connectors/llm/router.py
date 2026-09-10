import os
import time


PROVIDERS = {
    "openai": "OPENAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "gemini": "GEMINI_API_KEY",
}


def available_providers():
    results = {}

    if os.getenv("IMA_ENABLE_LOCAL_LLM") == "1":
        results["ollama"] = {
            "provider": "ollama",
            "status": "ready",
            "local": True,
        }

    for name, env in PROVIDERS.items():
        if os.getenv(env):
            results[name] = {
                "provider": name,
                "status": "ready",
                "credential_env": env,
                "local": False,
            }

    return results


def select_provider(preferred=None):
    available = available_providers()

    if preferred and preferred in available:
        return available[preferred]

    order = os.getenv(
        "IMA_PROVIDER_ORDER",
        "openai,anthropic,gemini,ollama"
    ).split(",")

    for name in order:
        name = name.strip()
        if name in available:
            return available[name]

    return {
        "provider": None,
        "status": "no_provider",
    }


def ask_models(message):
    return {
        "time": time.time(),
        "count": len(available_providers()),
        "models": available_providers(),
    }
