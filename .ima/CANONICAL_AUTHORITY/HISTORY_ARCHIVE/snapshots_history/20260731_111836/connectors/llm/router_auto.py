from .discovery_engine import discover
from .capability_test import rank


def choose_model():
    data=discover()

    models=data.get("local_models",[])

    if models:
        ranked=rank(
            [m["name"] for m in models]
        )

        best=ranked[0]

        return {
            "provider":"ollama",
            "model":best["model"],
            "score":best["score"],
            "source":"local"
        }

    clouds=[
        x for x in data.get("cloud",[])
        if x.get("configured")
    ]

    if clouds:
        return {
            "provider":clouds[0]["provider"],
            "source":"cloud"
        }

    return {
        "provider":"none",
        "source":"none"
    }
