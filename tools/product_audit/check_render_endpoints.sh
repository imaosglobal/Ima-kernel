#!/data/data/com.termux/files/usr/bin/bash

set -e

URL="https://ima-915m.onrender.com"
DATE=$(date +%Y%m%d_%H%M%S)

OUT=".ima/releases/render_activation/diagnostic_$DATE"
mkdir -p "$OUT"

python - <<PY
import urllib.request
import json
from pathlib import Path

base="$URL"

paths=[
"/",
"/health",
"/status",
"/version"
]

results=[]

for p in paths:
    item={"path":p}
    try:
        r=urllib.request.urlopen(base+p,timeout=30)
        body=r.read(300).decode(errors="ignore")
        item["status"]=r.status
        item["response"]=body
    except Exception as e:
        item["error"]=str(e)

    results.append(item)

Path("$OUT/ENDPOINT_MATRIX.json").write_text(
json.dumps(results,indent=2)
)

print(json.dumps(results,indent=2))
PY

echo "=== RENDER DIAGNOSTIC COMPLETE ==="
echo "$OUT"

