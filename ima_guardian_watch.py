from pathlib import Path
import subprocess
import time
import sys
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
        ["python3", "ima_guardian_master.py"]
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
    if "--status" in sys.argv:
        guardian_status()
    elif "--once" in sys.argv:
        run_cycle()
    elif "--daemon" in sys.argv:
        _original_watch()
    else:
        print("IMA Guardian Watch")
        print("use: --once | --daemon | --status")


# --- IMA Guardian modes ---

def guardian_status():
    print("=== IMA GUARDIAN STATUS ===")
    print("watcher:", Path("ima_guardian_watch.py").exists())
    print("controller:", Path("ima_guardian_master.py").exists())
    print("audit:", Path("IMA_AUDIT_REPORT.json").exists())


def run_once():
    import subprocess
    subprocess.run(
        ["python3", "ima_guardian_master.py"]
    )


_original_watch = watch

def watch_mode():
    if "--status" in sys.argv:
        guardian_status()
        return

    if "--once" in sys.argv:
        run_cycle()
        return

    _original_watch()


watch = watch_mode
