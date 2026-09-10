from pathlib import Path
import ast
import json
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]


def _python_files():
    skip = {".git", "node_modules", "__pycache__", "venv", ".venv"}
    for p in ROOT.rglob("*.py"):
        if not any(part in skip for part in p.parts):
            yield p


def _syntax_scan():
    broken = []

    for path in _python_files():
        try:
            ast.parse(path.read_text(encoding="utf-8"))
        except Exception as exc:
            broken.append({
                "file": str(path.relative_to(ROOT)),
                "error": type(exc).__name__,
                "message": str(exc),
            })

    return broken


def _git_state():
    try:
        result = subprocess.run(
            ["git", "status", "--short"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=20,
        )
        return result.stdout.splitlines()
    except Exception as exc:
        return [f"GIT_ERROR: {exc}"]


def run_self_improvement():
    started = time.time()

    broken = _syntax_scan()
    git_changes = _git_state()

    diagnosis = {
        "timestamp": time.time(),
        "duration": round(time.time() - started, 3),
        "python_files_checked": sum(1 for _ in _python_files()),
        "syntax_errors": broken,
        "git_changes": len(git_changes),
        "status": "issues_detected" if broken else "inspection_complete",
    }

    report_dir = ROOT / "learning" / "self_improvement_reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    report = report_dir / "latest_self_diagnosis.json"
    report.write_text(
        json.dumps(diagnosis, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    return diagnosis
