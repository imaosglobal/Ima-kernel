import json
import urllib.request
import time

def scan():
    result={
        "time":time.time(),
        "models":[]
    }

    try:
        data=urllib.request.urlopen(
            "http://127.0.0.1:11434/api/tags",
            timeout=3
        )
        obj=json.loads(data.read())

        for m in obj.get("models",[]):
            result["models"].append({
                "name":m.get("name"),
                "provider":"ollama",
                "status":"detected"
            })

    except Exception:
        pass

    return result


if __name__=="__main__":
