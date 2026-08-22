import urllib.request
import json
import time

def execute(model, prompt):
    try:
        payload=json.dumps({
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options":{
                "num_ctx":2048,
                "temperature":0.3
            }
        }).encode()

        req=urllib.request.Request(
            "http://127.0.0.1:11434/api/generate",
            data=payload,
            headers={"Content-Type":"application/json"}
        )

        with urllib.request.urlopen(req,timeout=40) as r:
            data=json.loads(r.read())

        return {
            "model":model,
            "response":data.get("response",""),
            "time":time.time()
        }

    except Exception as e:
        return {
            "model":model,
            "response":"",
            "error":str(e),
            "time":time.time()
        }
