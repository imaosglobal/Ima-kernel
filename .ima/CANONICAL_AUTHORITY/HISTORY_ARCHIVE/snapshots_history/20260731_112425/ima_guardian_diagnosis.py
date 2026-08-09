from pathlib import Path
import json
import subprocess
from datetime import datetime

ROOT = Path(".")

REPORT = Path("IMA_AUDIT_REPORT.json")
LOG = Path(".ima/guardian/master.log")
HISTORY = Path(".ima/guardian/history.jsonl")


def run(cmd):
    r = subprocess.run(
        cmd,
        shell=True,
        text=True,
        capture_output=True
    )
    return r.stdout.strip()


def load_json(path):
    if path.exists():
        try:
            return json.loads(
                path.read_text(encoding="utf8")
            )
        except:
            return {}
    return {}


def diagnose():

    result = {
        "time": datetime.now().isoformat(),
        "git": {},
        "audit": {},
        "guardian": {}
    }


    result["git"]["status"] = run(
        "git status --short"
    )

    result["git"]["branch"] = run(
        "git branch --show-current"
    )


    audit = load_json(REPORT)

    result["audit"] = {
        "python_files":
            audit.get("python_files"),
        "syntax_errors":
            audit.get("stats",{}).get(
                "syntax_errors"
            ),
        "duplicates":
            audit.get("stats",{}).get(
                "duplicate_groups"
            )
    }


    result["guardian"] = {
        "log_exists": LOG.exists(),
        "history_exists": HISTORY.exists(),
        "history_lines":
            sum(1 for _ in HISTORY.open())
            if HISTORY.exists()
            else 0
    }


    return result


if __name__ == "__main__":

    print(
        "=== IMA GUARDIAN DIAGNOSIS ==="
    )

    data = diagnose()

    print(
        json.dumps(
            data,
            indent=2,
            ensure_ascii=False
        )
    )
