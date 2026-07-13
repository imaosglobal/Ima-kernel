import json
import urllib.request

print("=== IMA CHAT ===")
print("כתוב exit ליציאה")

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

        print("\nIMA:")

        if "response" in answer:
            print(answer["response"])

        elif "identity_document" in answer:
            print(answer["identity_document"])

        else:
            print(json.dumps(answer, ensure_ascii=False, indent=2))

    except Exception as e:
        print("שגיאת חיבור:", e)
