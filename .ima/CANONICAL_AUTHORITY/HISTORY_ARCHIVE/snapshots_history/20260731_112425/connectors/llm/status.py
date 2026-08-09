import os

def status():
    return {
        "ollama": os.getenv("IMA_ENABLE_LOCAL_LLM") == "1",
        "openai": bool(os.getenv("OPENAI_API_KEY")),
        "anthropic": bool(os.getenv("ANTHROPIC_API_KEY")),
        "gemini": bool(os.getenv("GEMINI_API_KEY"))
    }
