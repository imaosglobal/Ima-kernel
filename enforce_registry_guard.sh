#!/data/data/com.termux/files/usr/bin/bash
set -e

FILE="IMA_START_SINGLE_ENTRY.py"
BACKUP="${FILE}.registry_backup.py"

cp "$FILE" "$BACKUP"

python3 - <<'PY'
from pathlib import Path

p=Path("IMA_START_SINGLE_ENTRY.py")
text=p.read_text()

guard='''

# CANONICAL REGISTRY ENFORCEMENT
from pathlib import Path
import hashlib, json

REG=Path(".ima/agi_evolution/runtime/CANONICAL_REGISTRY.json")

if not REG.exists():
    raise SystemExit("CANONICAL REGISTRY MISSING")

registry=json.loads(REG.read_text())

if registry.get("mode") != "canonical_only":
    raise SystemExit("INVALID CANONICAL MODE")

for item in registry.get("allowed_components", []):
    f=Path(item["file"])
    if not f.exists():
        raise SystemExit(f"MISSING CANONICAL COMPONENT: {f}")

    h=hashlib.sha256(f.read_bytes()).hexdigest()
    if h != item["sha256"]:
        raise SystemExit(f"HASH MISMATCH: {f}")

print("[OK] CANONICAL REGISTRY VERIFIED")
'''

marker='print("=== IMA SINGLE ENTRY ===")'

if "CANONICAL REGISTRY VERIFIED" not in text:
    text=text.replace(marker,guard+"\n"+marker)

p.write_text(text)
print("[OK] Registry guard injected")
PY

python3 IMA_START_SINGLE_ENTRY.py > logs/registry_guard_test.log 2>&1

grep -E "REGISTRY|POLICY|HASH|COMPLETE|KERNEL" logs/registry_guard_test.log

git add IMA_START_SINGLE_ENTRY.py IMA_START_SINGLE_ENTRY.registry_backup.py
git commit -m "Enforce canonical registry at boot"
git push

echo "=== REGISTRY ENFORCEMENT COMPLETE ==="
