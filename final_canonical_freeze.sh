#!/data/data/com.termux/files/usr/bin/bash
set -e

echo "=== IMA FINAL CANONICAL FREEZE ==="

python3 - <<'PY'
from pathlib import Path
import json
import hashlib
from datetime import datetime

root=Path(".")

canonical=[
".ima/runtime/runtime.py",
"learning/meta_orchestrator.py",
".ima/governance/canonical_architecture.json",
".ima/governance/CANONICAL_LOCK_FINAL.json"
]


for p in canonical:
    if not Path(p).exists():
        raise SystemExit(f"MISSING {p}")


bad=[]

for p in Path(".").rglob("*"):
    if not p.is_file():
        continue
    if ".git" in p.parts or "__pycache__" in p.parts:
        continue
    try:
        s=p.read_text(errors="ignore")
    except:
        continue

    for x in [
        "require('./ima_runtime.js')",
        "require('./ima_policy.js')",
        "require('./ima_kernel.js')"
    ]:
        if x in s and "_legacy_node_runtime" not in str(p):
            bad.append(str(p))

if bad:
    for b in bad:
    raise SystemExit(1)




h=hashlib.sha256()

for p in sorted(canonical):
    data=Path(p).read_bytes()
    h.update(data)

state={
"state":"FINAL_CANONICAL_LOCKED",
"canonical":canonical,
"sha256":h.hexdigest(),
"time":datetime.now().isoformat()
}

Path(".ima/governance/FINAL_CANONICAL_STATE.json").write_text(
json.dumps(state,indent=2)
)

PY

echo "=== FINAL CANONICAL FREEZE COMPLETE ==="
