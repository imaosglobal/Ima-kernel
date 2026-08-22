from pathlib import Path
import subprocess
import json
from datetime import datetime

ROOT = Path(".")
LOG = ROOT / ".ima/guardian/master.log"
LOG.parent.mkdir(parents=True, exist_ok=True)

CONTROLLER = "ima_guardian_controller.py"


def log(msg):
    with LOG.open("a", encoding="utf8") as f:
        f.write(
            f"{datetime.now().isoformat()} {msg}\n"
        )


def git_checkpoint(name):
    subprocess.run(
        ["git", "add", "-A"],
        capture_output=True
    )

    subprocess.run(
        ["git", "commit", "-m", name],
        capture_output=True
    )


def run_controller():
    if not Path(CONTROLLER).exists():
        log("[FAIL] controller missing")
        return False

    log("[RUN] guardian controller")

    r = subprocess.run(
        ["python3", CONTROLLER],
        text=True,
        capture_output=True
    )

    if r.returncode:
        log("[FAIL] guardian controller")
        log(r.stderr[-500:])
        return False

    log("[OK] guardian controller")
    return True


def compact_history():
    script = Path(".ima/guardian/history_compactor.py")

    if script.exists():
        subprocess.run(
            ["python3", str(script)]
        )
        log("[OK] history compacted")


def status():
    policy = Path(".ima/guardian/policy.json")



def cycle():
    log("=== MASTER CYCLE START ===")

    git_checkpoint(
        "guardian-master-before"
    )

    ok = run_controller()

    compact_history()

    if ok:
        git_checkpoint(
            "guardian-master-after"
        )

    log("=== MASTER CYCLE END ===")


if __name__ == "__main__":
    import sys

    if "--status" in sys.argv:
        status()
    else:
        cycle()


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
