from pathlib import Path
import subprocess
import json
from datetime import datetime

ROOT = Path(".")
REPORT = ROOT / "IMA_AUDIT_REPORT.json"
LOG = ROOT / ".ima" / "guardian" / "guardian_controller.log"

LOG.parent.mkdir(parents=True, exist_ok=True)


def log(msg):
    print(msg)
    with LOG.open("a", encoding="utf8") as f:
        f.write(
            f"{datetime.now().isoformat()} {msg}\n"
        )


def run(cmd):
    log("[RUN] " + cmd)

    r = subprocess.run(
        cmd,
        shell=True,
        text=True,
        capture_output=True
    )

    if r.returncode:
        log("[FAIL] " + r.stderr[-500:])
    else:
        log("[OK]")

    return r


def git_checkpoint(name):
    run("git add -A")
    run(f'git commit -m "{name}"')


def audit():
    run("python3 ima_full_audit.py")


def load_report():

    if REPORT.exists():
        return json.loads(
            REPORT.read_text(
                encoding="utf8"
            )
        )

    return {}


def run_autofix():

    p = ROOT / "ima_guardian_autofix.py"

    if not p.exists():
        log("[WARN] autofix missing")
        return

    run(
        "python3 ima_guardian_autofix.py"
    )


def validate():

    run(
        "python3 -m compileall learning"
    )


def cycle():

    log("=== IMA GUARDIAN CONTROLLER START ===")

    git_checkpoint(
        "guardian-before-cycle"
    )

    audit()

    report = load_report()

    errors = (
        report
        .get("stats", {})
        .get("syntax_errors", 0)
    )

    log(
        f"[AUDIT] syntax errors: {errors}"
    )

    run_autofix()

    validate()

    git_checkpoint(
        "guardian-after-cycle"
    )

    log(
        "=== IMA GUARDIAN CONTROLLER END ==="
    )


if __name__ == "__main__":
    cycle()
