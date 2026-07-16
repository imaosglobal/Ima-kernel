import json
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




def guardian_status():
    from pathlib import Path

    print("=== IMA GUARDIAN WATCH STATUS ===")

    data = {
        "controller": Path("ima_guardian_controller.py").exists(),
        "master": Path("ima_guardian_master.py").exists(),
        "policy": Path(".ima/guardian/policy.json").exists(),
        "history": Path(".ima/guardian/history.jsonl").exists(),
        "smart_state": Path(".ima/guardian/smart_state.json").exists()
    }

    for key, value in data.items():
        print(f"{key}: {value}")



def smart_diff():

    state = Path(".ima/guardian/smart_state.json")

    if not state.exists():
        return []

    old = json.loads(state.read_text(encoding="utf8"))
    changed = []

    for f, old_time in old.items():
        p = Path(f)
        if p.exists():
            try:
                if p.stat().st_mtime != old_time:
                    changed.append(f)
            except:
                pass

    return changed


def update_smart_state():

    state = Path(".ima/guardian/smart_state.json")
    data = {}

    for folder in ["ima","learning","runtime","api"]:
        p = Path(folder)
        if p.exists():
            for f in p.rglob("*.py"):
                if ".git" not in str(f):
                    try:
                        data[str(f)] = f.stat().st_mtime
                    except:
                        pass

    state.parent.mkdir(parents=True, exist_ok=True)
    state.write_text(
        json.dumps(data, indent=2),
        encoding="utf8"
    )




def incremental_cycle():

    changed = smart_diff()

    print("=== SMART INCREMENTAL CYCLE ===")
    print("[CHANGED]", len(changed))

    if not changed:
        print("[OK] nothing changed")
        return

    python_changed = [
        x for x in changed
        if x.endswith(".py")
    ]

    if len(python_changed) <= 5:

        import subprocess

        for f in python_changed:
            print("[CHECK]", f)

            subprocess.run(
                [
                    "python3",
                    "-m",
                    "py_compile",
                    f
                ]
            )

    else:
        print("[FULL AUDIT REQUIRED]")

        import subprocess

        subprocess.run(
            [
                "python3",
                "ima_guardian_master.py"
            ]
        )

    update_smart_state()


def run_cycle():

    print("\n=== GUARDIAN AUTO CYCLE ===")

    try:
        if "incremental_cycle" in globals():
            changed = incremental_cycle()

            if changed is False:
                print("[SMART STOP] no changes detected")
                return

            print("[OK] incremental cycle executed")
    except Exception as e:
        print("[INCREMENTAL ERROR]", e)

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

def guardian_incremental_check():
    import subprocess
    import py_compile

    print("=== GUARDIAN INCREMENTAL CHECK ===")

    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD"],
        capture_output=True,
        text=True
    )

    files = [
        x.strip()
        for x in result.stdout.splitlines()
        if x.endswith(".py")
    ]

    print("[CHANGED PYTHON]", len(files))

    errors=[]

    for f in files:
        try:
            py_compile.compile(
                f,
                doraise=True
            )
            print("[OK]", f)

        except Exception as e:
            print("[FAIL]", f)
            errors.append(f)

    if errors:
        print("[REPAIR TARGETS]")
        for e in errors:
            print(e)

        subprocess.run(
            ["python3","ima_guardian_self_repair.py"]
        )

    return len(errors)==0

