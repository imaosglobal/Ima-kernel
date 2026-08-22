import os
import json
import time
import urllib.request
from pathlib import Path

REGISTRY = Path(".ima/llm_registry.json")


def check_ollama():
    found=[]

    try:
        r=urllib.request.urlopen(
            "http://127.0.0.1:11434/api/tags",
            timeout=3
        )

        data=json.loads(r.read())

        for m in data.get("models",[]):
            found.append({
                "name":m.get("name"),
                "provider":"ollama",
                "local":True,
                "ready":True
            })

    except Exception:
        pass

    return found


def check_local_services():
    services=[]

    ports=[
        ("ollama",11434),
        ("lmstudio",1234),
        ("llamacpp",8080)
    ]

    for name,port in ports:
        try:
            urllib.request.urlopen(
                f"http://127.0.0.1:{port}",
                timeout=1
            )

            services.append({
                "provider":name,
                "local":True,
                "ready":True
            })

        except Exception:
            pass

    return services


def check_cloud():
    providers=[]

    keys={
        "openai":"OPENAI_API_KEY",
        "anthropic":"ANTHROPIC_API_KEY",
        "gemini":"GEMINI_API_KEY"
    }

    for name,key in keys.items():
        providers.append({
            "provider":name,
            "configured":bool(os.getenv(key))
        })

    return providers


def discover():
    result={
        "time":time.time(),
        "local_models":check_ollama(),
        "local_services":check_local_services(),
        "cloud":check_cloud()
    }

    REGISTRY.parent.mkdir(exist_ok=True)

    REGISTRY.write_text(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )

    return result


if __name__=="__main__":
