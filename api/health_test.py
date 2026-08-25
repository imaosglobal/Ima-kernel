import json
import urllib.request

for url in [
    "http://127.0.0.1:8080/health",
    "http://127.0.0.1:8080/",
]:
    try:
        r = urllib.request.urlopen(url)
        print(url, r.status)
        print(r.read().decode())
    except Exception as e:
        print(url, "ERROR:", e)

data = json.dumps({
    "message": "מי זאת IMA?"
}).encode()

req = urllib.request.Request(
    "http://127.0.0.1:8080/ask",
    data=data,
    headers={"Content-Type": "application/json"}
)

try:
    r = urllib.request.urlopen(req)
    print("/ask", r.status)
    print(r.read().decode())
except Exception as e:
    print("/ask ERROR:", e)
