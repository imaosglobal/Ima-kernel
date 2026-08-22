from pathlib import Path
import subprocess
from datetime import datetime

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("[FAILED]")
    return r

def tag_base():
    tag=f"ima-auto-base-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    run(["git","tag",tag])
    return tag

def verify():
    run(["python3","guardian_regression_check.py"])
    run(["python3","ima_guardian_watch.py","--once"])

def nightly_audit():
    import datetime
    hour = datetime.datetime.now().hour

    if hour == 3:
        run(["python3","ima_full_audit.py"])
    else:

def commit():
    run(["git","add","-A"])

    status = subprocess.run(
        ["git","diff","--cached","--quiet"]
    )

    if status.returncode == 0:
        return False

    msg=f"IMA automatic guarded commit {datetime.now().isoformat()}"
    run(["git","commit","-m",msg])
    return True

def final_tag():
    status = subprocess.run(
        ["git","rev-parse","--verify","HEAD"],
        capture_output=True
    )

    tag=f"ima-release-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    run(["git","tag",tag])

def main():

    tag_base()

    verify()

    changed = commit()

    if not changed:
        return

    final_tag()


if __name__=="__main__":
    main()
