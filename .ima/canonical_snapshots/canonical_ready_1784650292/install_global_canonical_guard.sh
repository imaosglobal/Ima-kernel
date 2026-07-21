#!/data/data/com.termux/files/usr/bin/bash
set -e

cat > canonical_guard.py <<'PY'
from pathlib import Path
import json, hashlib, sys

REG=Path(".ima/agi_evolution/runtime/CANONICAL_REGISTRY.json")

def verify():
    if not REG.exists():
        print("[BLOCK] CANONICAL REGISTRY MISSING")
        return False

    r=json.loads(REG.read_text())

    if r.get("mode")!="canonical_only":
        print("[BLOCK] INVALID MODE")
        return False

    for item in r.get("allowed_components",[]):
        p=Path(item["file"])

        if not p.exists():
            print("[BLOCK] MISSING:",p)
            return False

        h=hashlib.sha256(p.read_bytes()).hexdigest()

        if h != item["sha256"]:
            print("[BLOCK] HASH MISMATCH:",p)
            return False

    print("[OK] GLOBAL CANONICAL GUARD")
    return True

if __name__=="__main__":
    if not verify():
        sys.exit(1)
PY


cat > ima_canonical_run.sh <<'SH'
#!/data/data/com.termux/files/usr/bin/bash
set -e

cd "$(dirname "$0")"

python3 canonical_guard.py

exec "$@"
SH

chmod +x ima_canonical_run.sh

git add canonical_guard.py ima_canonical_run.sh install_global_canonical_guard.sh

git commit -m "Add global canonical guard for Termux and future entry points"

git push

echo "=== GLOBAL CANONICAL GUARD INSTALLED ==="
