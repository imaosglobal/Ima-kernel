from pathlib import Path
import subprocess
from datetime import datetime

def run(cmd):
    print("[RUN]", " ".join(cmd))
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(r.stdout)
    if r.returncode != 0:
        print(r.stderr)
        raise SystemExit("[FAILED]")
    return r

def tag_base():
    tag=f"ima-auto-base-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    run(["git","tag",tag])
    print("[BASE TAG]",tag)
    return tag

def verify():
    run(["python3","guardian_regression_check.py"])
    run(["python3","ima_guardian_watch.py","--once"])

def nightly_audit():
    import datetime
    hour = datetime.datetime.now().hour

    if hour == 3:
        print("[NIGHTLY AUDIT WINDOW]")
        run(["python3","ima_full_audit.py"])
    else:
        print("[SKIP FULL AUDIT] nightly only")

def commit():
    run(["git","add","-A"])

    status = subprocess.run(
        ["git","diff","--cached","--quiet"]
    )

    if status.returncode == 0:
        print("[NO CHANGES] commit skipped")
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
    print("[FINAL TAG]",tag)

def main():
    print("=== IMA GUARDED RELEASE PIPELINE ===")

    tag_base()

    verify()

    changed = commit()

    if not changed:
        print("[STOP] no release created")
        return

    final_tag()

    print("[DONE]")

if __name__=="__main__":
    main()
