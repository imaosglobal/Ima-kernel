#!/data/data/com.termux/files/usr/bin/bash

cd ~/ima_kernel

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
