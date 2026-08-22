from pathlib import Path
import json
import subprocess
import importlib.util

ROOT = Path(".")
GUARDIAN = ROOT / ".ima" / "guardian"

GUARDIAN.mkdir(parents=True, exist_ok=True)

REPORT = ROOT / "IMA_AUDIT_REPORT.json"


def run(cmd):
    return subprocess.run(
        cmd,
        shell=True,
        text=True,
        capture_output=True
    )


def git_checkpoint(name):
    run("git add -A")
    run(f'git commit -m "{name}"')


def load_audit():
    if REPORT.exists():
        return json.loads(REPORT.read_text(encoding="utf8"))
    return {}


def locate_autofix():
    candidates = [
        "ima_autofix.py",
        "ima_guardian_autofix.py",
        ".ima/guardian/autofix.py",
        "repair_all.py"
    ]

    for c in candidates:
        p = ROOT / c
        if p.exists():
            return p

    return None



git_checkpoint("guardian-before-autofix")

audit = load_audit()

    "Syntax errors:",
    audit.get("stats",{}).get("syntax_errors",0)
)

autofix = locate_autofix()

if not autofix:
else:

    spec = importlib.util.spec_from_file_location(
        "autofix",
        autofix
    )

    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    if hasattr(mod,"run"):
        mod.run()



git_checkpoint("guardian-after-autofix")

