import json
import time
from pathlib import Path
from .router import select_provider
from .model_registry import refresh, recommended

REGISTRY = Path(".ima/llm_selection.json")


def select(force=False):
    provider = select_provider()
    name = provider.get("provider")
    model = recommended(name) if name else None
    if name and not model:
        provider = {**provider, "status": "no_compatible_model"}
    selected = {"time": time.time(), "selected": provider, "provider": name if model else None, "model": model}
    REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY.write_text(json.dumps(selected, indent=2, ensure_ascii=False), encoding="utf8")
    return selected


def current():
    try:
        if REGISTRY.exists():
            data = json.loads(REGISTRY.read_text(encoding="utf8"))
            provider = data.get("provider")
            if provider:
                fresh = recommended(provider)
                if fresh and fresh != data.get("model"):
                    data["model"] = fresh
                    data["time"] = time.time()
                    REGISTRY.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf8")
                return data
    except Exception:
        pass
    return select()
