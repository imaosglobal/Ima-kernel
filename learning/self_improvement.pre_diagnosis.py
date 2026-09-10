from pathlib import Path
import ast
import json
import shutil
import subprocess
import time
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "learning" / "self_improvement_reports"
BACKUP_DIR = ROOT / "learning" / "self_improvement_backups"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
BACKUP_DIR.mkdir(parents=True, exist_ok=True)


def discover_python_files():
    excluded = {".git", "node_modules", "__pycache__", ".venv", "venv"}

    return [
        p for p in ROOT.rglob("*.py")
        if not any(part in excluded for part in p.parts)
    ]


def inspect_file(path):
    try:
        source = path.read_text(encoding="utf-8", errors="ignore")
        ast.parse(source)
        return {
            "file": str(path.relative_to(ROOT)),
            "valid": True,
            "error": None,
        }
    except Exception as exc:
        return {
            "file": str(path.relative_to(ROOT)),
            "valid": False,
            "error": f"{type(exc).__name__}: {exc}",
        }


def diagnose():
    files = discover_python_files()
    inspections = [inspect_file(p) for p in files]
    failures = [x for x in inspections if not x["valid"]]

    return {
        "files_checked": len(files),
        "syntax_failures": failures,
        "status": "issues_detected" if failures else "healthy",
    }


def create_backup(path):
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    backup = BACKUP_DIR / f"{path.name}.{stamp}.bak"
    shutil.copy2(path, backup)
    return backup


def validate_source(source):
    try:
        ast.parse(source)
        return {"valid": True, "error": None}
    except Exception as exc:
        return {
            "valid": False,
            "error": f"{type(exc).__name__}: {exc}",
        }


def rollback(path, backup):
    shutil.copy2(backup, path)


def verify_repository():
    return diagnose()


def record_learning(event):
    path = REPORT_DIR / "self_development_memory.jsonl"

    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def attempt_repair(path, diagnosis):
    """
    Conservative first repair strategy.

    Currently only performs structural indentation recovery when
    Python explicitly reports an unexpected indent. No semantic
    rewriting is attempted.
    """
    error = diagnosis.get("error", "")

    if "IndentationError" not in error:
        return {
            "status": "no_safe_repair",
            "reason": "No conservative repair strategy applies",
        }

    source = path.read_text(
        encoding="utf-8",
        errors="ignore",
    )

    lines = source.splitlines()

    repaired = []
    for line in lines:
        if line.strip() and line.startswith("    "):
            repaired.append(line[4:])
        else:
            repaired.append(line)

    candidate = "\n".join(repaired) + "\n"

    validation = validate_source(candidate)

    if not validation["valid"]:
        return {
            "status": "repair_rejected",
            "reason": validation["error"],
        }

    backup = create_backup(path)

    path.write_text(candidate, encoding="utf-8")

    post = inspect_file(path)

    if not post["valid"]:
        rollback(path, backup)

        return {
            "status": "rolled_back",
            "reason": post["error"],
            "backup": str(backup),
        }

    return {
        "status": "repaired",
        "file": str(path.relative_to(ROOT)),
        "backup": str(backup),
    }


def run_self_improvement():
    started = time.time()

    diagnosis = diagnose()
    repairs = []

    for failure in diagnosis["syntax_failures"]:
        path = ROOT / failure["file"]

        result = attempt_repair(
            path,
            failure,
        )

        repairs.append(result)

        record_learning({
            "timestamp": time.time(),
            "diagnosis": failure,
            "result": result,
        })

    final_state = verify_repository()

    report = {
        "timestamp": datetime.now().isoformat(),
        "duration": round(time.time() - started, 3),
        "initial": diagnosis,
        "repairs": repairs,
        "final": final_state,
        "status": (
            "improved"
            if len(final_state["syntax_failures"])
            < len(diagnosis["syntax_failures"])
            else "no_improvement"
        ),
    }

    report_path = REPORT_DIR / "latest_self_development.json"

    report_path.write_text(
        json.dumps(
            report,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    return report


if __name__ == "__main__":
    print(
        json.dumps(
            run_self_improvement(),
            indent=2,
            ensure_ascii=False,
        )
    )
