#!/usr/bin/env python3

import json
import os
import subprocess
import time
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.home() / "ima_kernel"
ORCH = ROOT / ".ima" / "ORCHESTRATION"
RUNTIME = ORCH / "runtime"
ENTRY = ORCH / "ima_orchestrator_entry.py"

STATE = RUNTIME / "automatic_cycle_state.json"
EVIDENCE = RUNTIME / "automatic_cycles"
EVIDENCE.mkdir(parents=True, exist_ok=True)

def now():
    return datetime.now(timezone.utc).isoformat()

state = {
    "schema": "ima.automatic.cycle.v1",
    "started_at": now(),
    "pid": os.getpid(),
    "cycles": 0,
}

if STATE.exists():
    try:
        old = json.loads(STATE.read_text())
        state.update(old)
    except Exception:
        pass

while True:
    state["cycles"] += 1
    cycle = state["cycles"]
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    result = {
        "schema": "ima.automatic.cycle.result.v1",
        "cycle": cycle,
        "timestamp": now(),
        "pid": os.getpid(),
        "source": "automatic_cycle_engine",
        "entry": str(ENTRY.relative_to(ROOT)),
    }

    try:
        proc = subprocess.run(
            ["python", str(ENTRY)],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=300,
        )

        result["returncode"] = proc.returncode
        result["stdout_tail"] = proc.stdout[-4000:]
        result["stderr_tail"] = proc.stderr[-4000:]
        result["status"] = "passed" if proc.returncode == 0 else "failed"

    except Exception as exc:
        result["status"] = "failed"
        result["error"] = repr(exc)

    out = EVIDENCE / f"cycle_{cycle:08d}_{ts}.json"
    out.write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    state["last_cycle"] = cycle
    state["last_status"] = result["status"]
    state["last_timestamp"] = result["timestamp"]
    STATE.write_text(
        json.dumps(state, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    if result["status"] != "passed":
        raise SystemExit(1)

    # Initial validation cadence: one cycle every 60 seconds.
    time.sleep(60)
