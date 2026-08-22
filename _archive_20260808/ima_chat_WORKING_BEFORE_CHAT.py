import json
import urllib.request


while True:
    msg = input("\nאתה: ")

    if msg.lower() in ["exit", "quit", "יציאה"]:
        break

    data = json.dumps({
        "message": msg
    }).encode()

    req = urllib.request.Request(
        "http://127.0.0.1:8080/ask",
        data=data,
        headers={"Content-Type": "application/json"}
    )

    try:
        res = urllib.request.urlopen(req)
        result = json.loads(res.read().decode())

        answer = result.get("answer", {})


        if "response" in answer:

        elif "identity_document" in answer:

        else:

    except Exception as e:
