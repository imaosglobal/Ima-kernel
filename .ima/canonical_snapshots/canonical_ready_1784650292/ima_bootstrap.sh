#!/usr/bin/env bash

set -e

echo "[IMA BOOTSTRAP] initializing event-driven kernel..."

mkdir -p .ima

# -----------------------
# LEDGER INIT
# -----------------------
touch .ima/ledger.jsonl

# -----------------------
# EVENT EMITTER
# -----------------------
cat > .ima/ima_event.py << 'PY'
import json, time

LEDGER = ".ima/ledger.jsonl"

def emit(event_type, **data):
    event = {
        "ts": time.time(),
        "type": event_type,
        "data": data
    }
    with open(LEDGER, "a") as f:
        f.write(json.dumps(event) + "\n")
PY

# -----------------------
# REDUCER (STATE ENGINE)
# -----------------------
cat > .ima/ima_reducer.py << 'PY'
import json

def reduce(events):
    state = {
        "files": set(),
        "mode": "INIT"
    }

    for e in events:
        t = e.get("type")
        d = e.get("data", {})

        if t == "FILE_ADD":
            state["files"].add(d.get("path"))

        elif t == "FILE_DELETE":
            state["files"].discard(d.get("path"))

        elif t == "KERNEL_REBUILD":
            state["mode"] = "REBUILT"

    state["files"] = list(state["files"])
    return state
PY

# -----------------------
# KERNEL CORE
# -----------------------
cat > ima_kernel.py << 'PY'
import json
from .ima_reducer import reduce

LEDGER = ".ima/ledger.jsonl"

def load_events():
    try:
        with open(LEDGER) as f:
            return [json.loads(l) for l in f if l.strip()]
    except:
        return []

def build_core():
    events = load_events()
    core = reduce(events)

    with open(".ima/core_map.json", "w") as f:
        json.dump(core, f, indent=2)

    return core

def status():
    core = build_core()

    print("=== IMA EVENT KERNEL ===")
    print("FILES:", len(core.get("files", [])))
    print("MODE:", core.get("mode"))

if __name__ == "__main__":
    status()
PY

# -----------------------
# GIT SNAPSHOT ENGINE
# -----------------------
cat > .ima/git_snapshot.sh << 'SH'
#!/usr/bin/env bash

STAMP=$(date +%s)

git add -A

if git diff --cached --quiet; then
    echo "[SNAPSHOT] nothing to commit"
    exit 0
fi

git commit -m "snapshot: $STAMP"
echo "[SNAPSHOT] committed $STAMP"
SH

chmod +x .ima/git_snapshot.sh

# -----------------------
# SYNC COMMAND
# -----------------------
cat > ima << 'SH'
#!/usr/bin/env bash

CMD=$1

case "$CMD" in
  status)
    python3 ima_kernel.py
    ;;
  sync)
    python3 ima_kernel.py >/dev/null 2>&1
    bash .ima/git_snapshot.sh
    ;;
  *)
    echo "IMA COMMANDS:"
    echo "  ima status"
    echo "  ima sync"
    ;;
esac
SH

chmod +x ima

echo "[IMA BOOTSTRAP] DONE"
echo "Run: ./ima status"
