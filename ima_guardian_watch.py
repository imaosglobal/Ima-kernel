from pathlib import Path
import subprocess
import time
import hashlib

ROOT = Path(".")
STATE = Path(".ima/guardian/watch_state")

STATE.parent.mkdir(parents=True, exist_ok=True)


def fingerprint():
    h = hashlib.sha256()

    for p in sorted(ROOT.rglob("*.py")):
        if any(x in str(p) for x in [
            ".git",
            ".ima/backups",
            "__pycache__"
        ]):
            continue

        try:
            h.update(str(p).encode())
            h.update(p.read_bytes())
        except:
            pass

    return h.hexdigest()


def run_cycle():

    print("\n=== GUARDIAN AUTO CYCLE ===")

    subprocess.run(
        ["python3", "ima_guardian_controller.py"]
    )


def watch():

    old = None

    if STATE.exists():
        old = STATE.read_text()

    while True:

        current = fingerprint()

        if current != old:

            print("[CHANGE DETECTED]")

            run_cycle()

            STATE.write_text(current)
            old = current

        time.sleep(30)


if __name__ == "__main__":
    watch()
