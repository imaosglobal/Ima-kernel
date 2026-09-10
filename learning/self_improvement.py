from pathlib import Path
import ast
import hashlib
import json
import shutil
import subprocess
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "learning" / "self_improvement_reports"
BACKUP_DIR = ROOT / "learning" / "self_improvement_backups"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
BACKUP_DIR.mkdir(parents=True, exist_ok=True)


def discover_python_files():
    excluded = {
        ".git",
        "node_modules",
        "__pycache__",
        ".venv",
        "venv",
        "dist",
    }

    return [
        p for p in ROOT.rglob("*.py")
        if not any(part in excluded for part in p.parts)
    ]


def inspect_file(path):
    source = path.read_text(errors="replace")

    try:
        ast.parse(source)
        return {
            "file": str(path.relative_to(ROOT)),
            "valid": True,
            "error": None,
            "line": None,
            "column": None,
        }

    except SyntaxError as exc:
        return {
            "file": str(path.relative_to(ROOT)),
            "valid": False,
            "error": f"{type(exc).__name__}: {exc}",
            "line": exc.lineno,
            "column": exc.offset,
        }

    except Exception as exc:
        return {
            "file": str(path.relative_to(ROOT)),
            "valid": False,
            "error": f"{type(exc).__name__}: {exc}",
            "line": None,
            "column": None,
        }


def diagnose():
    files = discover_python_files()
    inspections = [inspect_file(p) for p in files]
    failures = [item for item in inspections if not item["valid"]]

    return {
        "files_checked": len(files),
        "syntax_failures": failures,
        "status": "issues_detected" if failures else "healthy",
    }


def validate_source(source):
    try:
        ast.parse(source)
        return {"valid": True, "error": None}
    except SyntaxError as exc:
        return {
            "valid": False,
            "error": f"{type(exc).__name__}: {exc}",
        }


def run_validation(path):
    result = subprocess.run(
        ["python3", "-m", "py_compile", str(path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=30,
    )

    return {
        "passed": result.returncode == 0,
        "stdout": result.stdout[-2000:],
        "stderr": result.stderr[-2000:],
        "returncode": result.returncode,
    }


def file_sha256(path):
    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()


def capture_before_state(path):
    return {
        "file": str(path.relative_to(ROOT)),
        "sha256": file_sha256(path),
        "size": path.stat().st_size,
    }


def capture_after_state(path, before):
    return {
        "file": str(path.relative_to(ROOT)),
        "before_sha256": before["sha256"],
        "after_sha256": file_sha256(path),
        "before_size": before["size"],
        "after_size": path.stat().st_size,
        "changed": before["sha256"] != file_sha256(path),
    }


def find_related_tests(path):
    candidates = []

    stem = path.stem
    parent = path.parent

    patterns = [
        f"test_{stem}.py",
        f"{stem}_test.py",
    ]

    for name in patterns:
        candidate = parent / name
        if candidate.exists():
            candidates.append(candidate)

    test_dir = parent / "tests"

    if test_dir.exists():
        for name in patterns:
            candidate = test_dir / name
            if candidate.exists():
                candidates.append(candidate)

    return list(dict.fromkeys(candidates))


def run_behavioral_tests(path):
    tests = find_related_tests(path)

    results = []

    for test in tests:
        result = subprocess.run(
            ["python3", str(test)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=60,
        )

        results.append({
            "test": str(test.relative_to(ROOT)),
            "passed": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout[-2000:],
            "stderr": result.stderr[-2000:],
        })

    if not tests:
        return {
            "mode": "compile_only",
            "passed": True,
            "tests": [],
            "reason": "No related test file found",
        }

    return {
        "mode": "related_tests",
        "passed": all(x["passed"] for x in results),
        "tests": results,
    }


def create_backup(path):
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    backup = BACKUP_DIR / f"{path.name}.{stamp}.bak"
    shutil.copy2(path, backup)
    return backup


def rollback(path, backup):
    shutil.copy2(backup, path)


def record_learning(event):
    memory = REPORT_DIR / "self_development_memory.jsonl"

    with memory.open("a", encoding="utf-8") as f:
        f.write(
            json.dumps(
                event,
                ensure_ascii=False,
                default=str,
            )
            + "\n"
        )


def repair_assignment_comment(path, diagnosis):
    line_no = diagnosis.get("line")

    if not line_no:
        return {
            "status": "no_safe_repair",
            "reason": "SyntaxError has no usable line number",
        }

    lines = path.read_text(errors="replace").splitlines()

    if not (1 <= line_no <= len(lines)):
        return {
            "status": "no_safe_repair",
            "reason": "Reported line is outside file",
        }

    line = lines[line_no - 1]

    if "=" not in line:
        return {
            "status": "no_safe_repair",
            "reason": "No assignment detected",
        }

    lhs, rhs = line.split("=", 1)

    if not rhs.lstrip().startswith("#"):
        return {
            "status": "no_safe_repair",
            "reason": "Assignment is not followed by a comment",
        }

    comment = rhs.split("#", 1)[1].strip()

    if not comment:
        return {
            "status": "no_safe_repair",
            "reason": "Comment contains no recoverable expression",
        }

    candidate_line = f"{lhs.rstrip()} = {comment}"

    candidate_lines = list(lines)
    candidate_lines[line_no - 1] = candidate_line
    candidate = "\n".join(candidate_lines) + "\n"

    validation = validate_source(candidate)

    if not validation["valid"]:
        return {
            "status": "repair_rejected",
            "reason": validation["error"],
            "strategy": "assignment_comment_recovery",
        }

    backup = create_backup(path)
    path.write_text(candidate, encoding="utf-8")

    post = inspect_file(path)
    test = run_validation(path)
    behavioral = run_behavioral_tests(path)

    changed = (
        before_state["sha256"] != file_sha256(path)
    )

    if post["valid"] and test["passed"] and behavioral["passed"] and changed:
        return {
            "status": "repaired",
            "file": str(path.relative_to(ROOT)),
            "line": line_no,
            "strategy": "assignment_comment_recovery",
            "backup": str(backup),
            "validation": test,
            "behavioral_tests": behavioral,
        }

    rollback(path, backup)

    return {
        "status": "rolled_back",
        "file": str(path.relative_to(ROOT)),
        "line": line_no,
        "reason": "Post-repair validation failed",
        "validation": test,
    }


def repair_indentation(path, diagnosis):
    source = path.read_text(errors="replace")
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
            "strategy": "indentation_recovery",
        }

    backup = create_backup(path)
    path.write_text(candidate, encoding="utf-8")

    post = inspect_file(path)
    test = run_validation(path)
    behavioral = run_behavioral_tests(path)

    changed = (
        before_state["sha256"] != file_sha256(path)
    )

    if post["valid"] and test["passed"] and behavioral["passed"] and changed:
        return {
            "status": "repaired",
            "file": str(path.relative_to(ROOT)),
            "strategy": "indentation_recovery",
            "backup": str(backup),
            "validation": test,
            "behavioral_tests": behavioral,
        }

    rollback(path, backup)

    return {
        "status": "rolled_back",
        "file": str(path.relative_to(ROOT)),
        "reason": "Post-repair validation failed",
        "validation": test,
    }


def load_strategy_history():
    memory = REPORT_DIR / "self_development_memory.jsonl"

    if not memory.exists():
        return []

    outcomes = []

    for line in memory.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue

        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue

        result = event.get("result", {})

        if result.get("status") == "repaired":
            outcomes.append({
                "file": result.get("file"),
                "strategy": result.get("strategy"),
                "validation_passed": (
                    result.get("validation", {}).get("passed", True)
                    if "validation" in result
                    else result.get("status") == "repaired"
                ),
                "behavioral_passed": (
                    result.get("behavioral_tests", {}).get("passed", True)
                    if "behavioral_tests" in result
                    else result.get("status") == "repaired"
                ),
                "behavioral_legacy": "behavioral_tests" not in result,
            })

    return outcomes


def strategy_score(strategy):
    history = load_strategy_history()

    matching = [
        item for item in history
        if item.get("strategy") == strategy
    ]

    if not matching:
        return 0.0

    successful = [
        item for item in matching
        if item.get("validation_passed") and item.get("behavioral_passed")
    ]

    return len(successful) / len(matching)


def attempt_repair(path, diagnosis):
    before_state = capture_before_state(path)
    error = diagnosis.get("error", "")

    if "SyntaxError" in error:
        result = repair_assignment_comment(path, diagnosis)
        result["before_state"] = before_state
        if result.get("status") == "repaired":
            result["after_state"] = capture_after_state(path, before_state)

        if result["status"] != "no_safe_repair":
            return result

    if "IndentationError" in error:
        result = repair_indentation(path, diagnosis)
        result["before_state"] = before_state
        if result.get("status") == "repaired":
            result["after_state"] = capture_after_state(path, before_state)
        return result

    return {
        "status": "no_safe_repair",
        "reason": "No validated repair strategy applies",
    }


def verify_repository():
    return diagnose()


def run_self_improvement():
    started = datetime.now()

    initial = diagnose()
    repairs = []
    rolled_back_files = []

    for failure in initial["syntax_failures"]:
        path = ROOT / failure["file"]

        result = attempt_repair(path, failure)
        repairs.append(result)

        record_learning({
            "timestamp": datetime.now().isoformat(),
            "diagnosis": failure,
            "result": result,
        })

    final = verify_repository()

    initial_count = len(initial["syntax_failures"])
    final_count = len(final["syntax_failures"])

    # Transactional safety:
    # if the complete repair cycle made the repository worse,
    # restore every successful repair from this cycle.
    if final_count > initial_count:
        rolled_back = []

        for repair in repairs:
            if repair.get("status") != "repaired":
                continue

            backup = repair.get("backup")
            file_name = repair.get("file")

            if not backup or not file_name:
                continue

            target = ROOT / file_name
            backup_path = Path(backup)

            if backup_path.exists():
                shutil.copy2(backup_path, target)
                rolled_back.append(file_name)

        if rolled_back:
            rolled_back_files.extend(rolled_back)
            final = verify_repository()
            final_count = len(final["syntax_failures"])

            record_learning({
                "timestamp": datetime.now().isoformat(),
                "event": "transaction_rollback",
                "files": rolled_back,
                "reason": "repair_cycle_increased_repository_errors",
                "initial_errors": initial_count,
                "final_errors_before_rollback": len(
                    verify_repository()["syntax_failures"]
                ),
            })

        status = "rolled_back"
    elif final_count == 0:
        status = "healthy"
    elif final_count < initial_count:
        status = "improved"
    else:
        status = "no_improvement"

    strategy_outcomes = []

    for repair in repairs:
        if repair.get("status") != "repaired":
            continue

        validation = repair.get("validation", {})
        behavioral = repair.get("behavioral_tests", {})

        strategy_outcomes.append({
            "file": repair.get("file"),
            "strategy": repair.get("strategy"),
            "validation_passed": validation.get("passed", False),
            "behavioral_passed": behavioral.get("passed", False),
            "behavioral_mode": behavioral.get("mode"),
            "tests_run": len(behavioral.get("tests", [])),
        })

    report = {
        "timestamp": started.isoformat(),
        "duration": (datetime.now() - started).total_seconds(),
        "initial": initial,
        "repairs": repairs,
        "strategy_outcomes": strategy_outcomes,
        "rolled_back_files": rolled_back_files,
        "final": final,
        "status": status,
    }

    (REPORT_DIR / "latest_self_development.json").write_text(
        json.dumps(
            report,
            indent=2,
            ensure_ascii=False,
            default=str,
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
