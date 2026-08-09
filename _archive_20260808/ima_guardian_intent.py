from pathlib import Path
import subprocess
import json
from datetime import datetime

LOG = Path(".ima/guardian/intent_history.jsonl")


def record(goal, result):
    LOG.parent.mkdir(parents=True, exist_ok=True)

    with LOG.open("a", encoding="utf8") as f:
        f.write(json.dumps({
            "time": datetime.now().isoformat(),
            "goal": goal,
            "result": result
        }, ensure_ascii=False) + "\n")


def execute(goal):

    print("=== IMA INTENT ENGINE ===")
    print("[GOAL]", goal)

    if "audit" in goal or "stability" in goal:
        cmd = ["python3", "ima_guardian_master.py"]
    else:
        cmd = ["python3", "ima_guardian_diagnosis.py"]

    r = subprocess.run(
        cmd,
        text=True,
        capture_output=True
    )

    result = "OK" if r.returncode == 0 else "FAIL"

    record(goal, result)

    print("[RESULT]", result)

    if r.stdout:
        print(r.stdout[-1000:])

    if r.stderr:
        print(r.stderr[-500:])


if __name__ == "__main__":
    execute(" ".join(__import__("sys").argv[1:]) or "stability audit")
