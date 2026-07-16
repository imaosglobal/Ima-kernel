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
    print("[RUN]", cmd)

    r = subprocess.run(
        cmd,
        shell=True,
        text=True,
        capture_output=True
    )

    if r.returncode:
        print("[FAIL]")
        print(r.stderr[-500:])
        record("failure", {"cmd":cmd})
        return False

    print("[OK]")
    record("success", {"cmd":cmd})
    return True


def cycle(goal="maintenance"):

    print("=== IMA GUARDIAN CORE ===")

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
