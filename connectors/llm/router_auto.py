from .discovery_engine import discover
from .capability_test import rank


def choose_model():
    data = discover()

    android_apps = data.get("android_apps", [])

    if android_apps:
        app = android_apps[0]
        return {
            "provider": app["provider"],
            "package": app["package"],
            "source": "android_app",
        }

    models = data.get("local_models", [])

    if models:
        ranked = rank([m["name"] for m in models])
        if ranked:
            best = ranked[0]
            return {
                "provider": "ollama",
                "model": best["model"],
                "score": best["score"],
                "source": "local",
            }

    clouds = [
        x for x in data.get("cloud", [])
        if x.get("configured")
    ]

    if clouds:
        return {
            "provider": clouds[0]["provider"],
            "source": "cloud",
        }

    return {
        "provider": "none",
        "source": "none",
    }
