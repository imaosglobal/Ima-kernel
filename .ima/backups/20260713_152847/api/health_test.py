import json
import urllib.request

print("=== IMA API TEST ===")

for url in [
    "http://127.0.0.1:8080/health",
    "http://127.0.0.1:8080/"
]:
    try:
        r=urllib.request.urlopen(url)
        print("[OK]",url)
        print(r.read().decode()[:500])
    except Exception as e:
        print("[FAIL]",url,e)

data=json.dumps({
    "message":"מי זאת IMA?"
}).encode()

req=urllib.request.Request(
    "http://127.0.0.1:8080/ask",
    data=data,
    headers={"Content-Type":"application/json"}
)

try:
    r=urllib.request.urlopen(req)
    print("[OK] BRAIN RESPONSE")
    print(r.read().decode()[:1000])
except Exception as e:
    print("[FAIL] ASK",e)
