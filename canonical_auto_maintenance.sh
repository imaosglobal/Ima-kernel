#!/data/data/com.termux/files/usr/bin/bash

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

find . -type d -name "__pycache__" -prune -exec rm -rf {} +
find . -name "*.pyc" -delete
find . -name "*.pid" -delete

python3 - <<'PY'
from pathlib import Path
import json,time

p=Path(".ima/runtime/maintenance_state.json")

p.write_text(json.dumps({
"last_cleanup":time.time(),
"status":"AUTO_MAINTENANCE_ACTIVE"
},indent=2))

print("[AUTO MAINTENANCE OK]")
PY
