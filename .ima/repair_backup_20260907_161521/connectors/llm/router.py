import os
import time

def ask_models(message):
    results = {}

    # Local Ollama - רק אם מופעל
    if os.getenv("IMA_ENABLE_LOCAL_LLM") == "1":
        try:
            from .ollama import ask as ollama_ask
            local = ollama_ask(message)
            if local.get("status") != "disabled":
                results["ollama"] = local
        except Exception as e:
            results["ollama_error"] = str(e)

    # External API readiness
    providers = {
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "gemini": "GEMINI_API_KEY"
    }

    for name, env in providers.items():
        if os.getenv(env):
            results[name] = {
                "status": "ready",
                "provider": name
            }

    return {
        "time": time.time(),
        "count": len(results),
        "models": results
    }
