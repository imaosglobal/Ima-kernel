#!/usr/bin/env bash

set -e

echo "[IMA UNIFIED BOOTSTRAP] starting..."

mkdir -p .ima

# =========================
# LEDGER
# =========================
touch .ima/ledger.jsonl

# =========================
# EVENT SYSTEM
# =========================
cat > ima_event.py << 'PY'
import json, time

LEDGER=".ima/ledger.jsonl"

def emit(t, **data):
    e = {"ts": time.time(), "type": t, "data": data}
    with open(LEDGER, "a") as f:
        f.write(json.dumps(e) + "\n")
PY

# =========================
# REDUCER
# =========================
cat > ima_reducer.py << 'PY'
import json

def reduce(events):
    state = {"files": set(), "mode": "INIT"}

    for e in events:
        t = e.get("type")
        d = e.get("data", {})

        if t == "FILE_ADD":
            state["files"].add(d.get("path"))

        if t == "FILE_REMOVE":
            state["files"].discard(d.get("path"))

        if t == "RESET":
            state["mode"] = "RESET"

    state["files"] = sorted(list(state["files"]))
    return state
PY

# =========================
# CORE KERNEL
# =========================
cat > ima_kernel.py << 'PY'
import json
from ima_reducer import reduce

LEDGER=".ima/ledger.jsonl"

def load():
    try:
        return [json.loads(l) for l in open(LEDGER) if l.strip()]
    except:
        return []

def status():
    events = load()
    state = reduce(events)

    print("=== IMA UNIFIED KERNEL ===")
    print("FILES:", len(state["files"]))
    print("MODE:", state["mode"])

if __name__ == "__main__":
    status()
PY

# =========================
# SNAPSHOT ENGINE
# =========================
cat > ima_snapshot.sh << 'SH'
#!/usr/bin/env bash

git add -A

if git diff --cached --quiet; then
  echo "[SNAPSHOT] no changes"
  exit 0
fi

STAMP=$(date +%s)
git commit -m "ima snapshot $STAMP"
echo "[SNAPSHOT] $STAMP"
SH

chmod +x ima_snapshot.sh

# =========================
# CLI
# =========================
cat > ima << 'SH'
#!/usr/bin/env bash

case "$1" in
  status)
    python3 ima_kernel.py
    ;;

  emit)
    python3 - <<PY
from ima_event import emit
import sys
emit(sys.argv[1], path=sys.argv[2])
PY
    "$2" "$3"
    ;;

  snapshot)
    bash ima_snapshot.sh
    ;;

  *)
    echo "ima status | emit | snapshot"
    ;;
esac
SH

chmod +x ima

# =========================
# GIT HOOK (SELF-HEALING)
# =========================
mkdir -p .git/hooks

cat > .git/hooks/pre-commit << 'EOF'
#!/usr/bin/env bash

python3 ima_kernel.py >/dev/null 2>&1 || exit 1
bash ima_snapshot.sh >/dev/null 2>&1
