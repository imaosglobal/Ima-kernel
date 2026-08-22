from pathlib import Path
import subprocess
import json
from datetime import datetime

LOG = Path(".ima/guardian/core_history.jsonl")
LOG.parent.mkdir(parents=True, exist_ok=True)


def record(event, data=None):
    row = {
        "time": datetime.now().isoformat(),
        "event": event,
        "data": data or {}
    }

    with LOG.open("a", encoding="utf8") as f:
        f.write(json.dumps(row, ensure_ascii=False)+"\n")


def run(cmd):

    r = subprocess.run(
        cmd,
        shell=True,
        text=True,
        capture_output=True
    )

    if r.returncode:
        record("failure", {"cmd":cmd})
        return False

    record("success", {"cmd":cmd})
    return True


def cycle(goal="maintenance"):


    record(
        "intent_start",
        {"goal":goal}
    )

    steps = [

        "python3 ima_guardian_master.py",

        "python3 ima_full_audit.py",
        "python3 ima_guardian_self_repair.py",

        "python3 ima_guardian_diagnosis.py"

    ]

    for s in steps:
        run(s)


    subprocess.run(
        "git add -A",
        shell=True
    )

    subprocess.run(
        f'git commit -m "guardian auto cycle {goal}"',
        shell=True
    )

    record(
        "intent_complete",
        {"goal":goal}
    )


if __name__ == "__main__":

    import sys

    goal=" ".join(sys.argv[1:]) or "maintenance"

    cycle(goal)


# IMA_SMART_MODE

from pathlib import Path
import json
import time


SMART_STATE = Path(".ima/guardian/smart_state.json")


def smart_snapshot():

    result = {}

    for folder in [
        "ima",
        "learning",
        "runtime",
        "api"
    ]:

        p = Path(folder)

        if not p.exists():
            continue

        for f in p.rglob("*.py"):

            if ".git" in str(f):
                continue

            if "__pycache__" in str(f):
                continue

            try:
                result[str(f)] = f.stat().st_mtime
            except:
                pass

    return result


def smart_changed():

    current = smart_snapshot()

    old = {}

    if SMART_STATE.exists():

        try:
            old=json.loads(
                SMART_STATE.read_text()
            )

        except:
            pass


    SMART_STATE.parent.mkdir(
        parents=True,
        exist_ok=True
    )


    SMART_STATE.write_text(
        json.dumps(current)
    )


    return [
        x for x in current
        if old.get(x)!=current[x]
    ]
