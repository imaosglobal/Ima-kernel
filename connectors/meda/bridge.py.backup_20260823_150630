from __future__ import annotations
import sys

import json
import subprocess
from datetime import datetime
from pathlib import Path


BASE = Path(__file__).resolve().parents[2]
MEDA = BASE / "external" / "MEDA"
SESSIONS = MEDA / "sessions"


def available() -> bool:
    return (
        MEDA.exists()
        and (MEDA / "skills" / "meda" / "scripts" / "main.py").exists()
    )


def status() -> dict:
    return {
        "available": available(),
        "meda_path": str(MEDA),
        "sessions_path": str(SESSIONS),
        "timestamp": datetime.now().isoformat(),
    }


def create_session(question: str) -> Path:
    if not available():
        raise RuntimeError(
            f"MEDA is not available at {MEDA}"
        )

    SESSIONS.mkdir(parents=True, exist_ok=True)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session = SESSIONS / f"ima_{stamp}"
    session.mkdir(parents=True, exist_ok=False)

    context = {
        "source": "IMA",
        "created_at": datetime.now().isoformat(),
        "question": question,
    }

    (session / "ima_context.json").write_text(
        json.dumps(context, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    (session / "context.md").write_text(
        "# IMA → MEDA Research Task\n\n"
        + question
        + "\n",
        encoding="utf-8",
    )

    return session


def meda_environment_ready() -> bool:
    """
    Check whether the MEDA CORE runtime is usable.

    MEDA has optional/full-CLI dependencies such as pandas,
    matplotlib, sklearn and zss. They are intentionally not
    required for the core symbolic discovery engine.

    Do not trigger uv or pip dependency resolution here.
    """
    required = [
        "numpy",
        "scipy",
        "yaml",
    ]

    for module in required:
        result = subprocess.run(
            [sys.executable, "-c", f"import {module}"],
            cwd=str(MEDA),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        if result.returncode != 0:
            return False

    core_scripts = MEDA / "skills" / "meda" / "scripts"

    required_files = [
        "constants.py",
        "term_parser.py",
        "equations.py",
        "regularization.py",
        "ga.py",
        "tuning.py",
    ]

    return all((core_scripts / name).is_file() for name in required_files)


def meda_full_environment_ready() -> bool:
    """
    Check the optional/full MEDA runtime.

    This requires the heavier data-analysis/reporting stack.
    It must never be installed implicitly by IMA.
    """
    required = [
        "numpy",
        "scipy",
        "yaml",
        "pandas",
        "matplotlib",
        "zss",
    ]

    for module in required:
        result = subprocess.run(
            [sys.executable, "-c", f"import {module}"],
            cwd=str(MEDA),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        if result.returncode != 0:
            return False

    return True


def run_meda(
    setup: str,
    problem: str,
    output: str,
) -> subprocess.CompletedProcess:
    """
    Run MEDA only when its isolated environment already exists.

    IMPORTANT:
    This function deliberately does NOT call `uv run`.
    That prevents IMA from unexpectedly rebuilding MEDA's
    scientific dependency stack on the Android device.
    """

    if not meda_environment_ready():
        raise RuntimeError(
            "MEDA environment is not ready. "
            "The MEDA .venv exists only partially or is not installed."
        )

    python = MEDA / ".venv" / "bin" / "python"

    command = [
        str(python),
        "skills/meda/scripts/main.py",
        "--setup",
        setup,
        "--problem",
        problem,
        "--output",
        output,
    ]

    return subprocess.run(
        command,
        cwd=str(MEDA),
        text=True,
        capture_output=True,
    )

def read_json(path: str | Path) -> dict:
    path = Path(path)

    if not path.exists():
        return {
            "ok": False,
            "error": "file_not_found",
            "path": str(path),
        }

    try:
        return {
            "ok": True,
            "path": str(path),
            "data": json.loads(
                path.read_text(encoding="utf-8")
            ),
        }
    except Exception as exc:
        return {
            "ok": False,
            "error": str(exc),
            "path": str(path),
        }


def investigate(question: str, context: dict | None = None) -> dict:
    """
    IMA -> MEDA research boundary.

    Creates a MEDA research session without importing MEDA's
    heavy scientific dependencies into the IMA runtime.
    """
    session = create_session(question)

    payload = {
        "ok": True,
        "question": question,
        "session": str(session),
        "environment_ready": meda_environment_ready(),
        "status": status(),
    }

    if context:
        payload["context"] = context

    return payload
