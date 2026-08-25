import os
import json
import time
import urllib.request

def scan_ollama():
    models=[]

    try:
        r=urllib.request.urlopen(
            "http://127.0.0.1:11434/api/tags",
            timeout=3
        )

        data=json.loads(r.read())

        for m in data.get("models",[]):
            models.append({
                "name":m.get("name"),
                "provider":"ollama",
                "type":"local",
                "status":"detected"
            })

    except Exception:
        pass

    return models


def scan_cloud():
    providers=[]

    checks=[
        ("openai","OPENAI_API_KEY"),
        ("anthropic","ANTHROPIC_API_KEY"),
        ("gemini","GEMINI_API_KEY")
    ]

    for name,key in checks:
        providers.append({
            "provider":name,
            "type":"cloud",
            "available":bool(os.getenv(key)),
            "status":"ready" if os.getenv(key) else "not_configured"
        })

    return providers


def scan_all():
    return {
        "time":time.time(),
        "local_models":scan_ollama(),
        "cloud_providers":scan_cloud()
    }


if __name__=="__main__":
    print(json.dumps(scan_all(),indent=2,ensure_ascii=False))
