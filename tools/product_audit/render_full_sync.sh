#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== IMA RENDER FULL SYNC ==="

ROOT="$HOME/ima_kernel"
cd "$ROOT"

DATE=$(date +%Y%m%d_%H%M%S)
OUT=".ima/releases/render_sync/$DATE"

mkdir -p "$OUT"


echo "[1] Fix Render configuration"

cat > render.yaml <<'EOF'
services:
  - type: web
    name: ima-915m
    runtime: docker
    plan: free
    dockerfilePath: ./Dockerfile
    healthCheckPath: /health
EOF


echo "[2] Fix API dynamic PORT"

python3 - <<'PY'
from pathlib import Path

p=Path("api/server.py")

s=p.read_text()

if "import os" not in s:
    s=s.replace("import sys","import sys\nimport os")

s=s.replace(
'HTTPServer(("0.0.0.0",8080),Handler).serve_forever()',
'PORT=int(os.environ.get("PORT",8080))\nHTTPServer(("0.0.0.0",PORT),Handler).serve_forever()'
)

p.write_text(s)

PY


echo "[3] Git sync"

git add render.yaml api/server.py

git commit -m "Render production synchronization fix" || true

git push


echo "[4] Local health"

curl -s http://127.0.0.1:8080/health \
 > "$OUT/local_health.json" || true


echo "[5] Render health"

curl \
--connect-timeout 10 \
--max-time 30 \
-i \
https://ima-915m.onrender.com/health \
> "$OUT/render_health.txt" || true


echo "[6] Status report"

cat > "$OUT/REPORT.json" <<EOF
{
 "service":"ima-915m",
 "url":"https://ima-915m.onrender.com",
 "timestamp":"$DATE",
 "git":"synced",
 "render":"checked"
}
EOF


echo
echo "OUTPUT:"
echo "$OUT"

echo
echo "=== COMPLETE ==="
