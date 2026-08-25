from __future__ import annotations
import sys

import json
import subprocess
import yaml
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
    data: str | None = None,
) -> subprocess.CompletedProcess:
    """Run the isolated MEDA discovery engine without implicit dependency installation."""
    if not meda_environment_ready():
        raise RuntimeError(
            "MEDA environment is not ready. "
            "Required scientific dependencies are missing."
        )

    venv_python = MEDA / ".venv" / "bin" / "python"
    python = venv_python if venv_python.is_file() else Path(sys.executable)

    # MEDA defaults to constraint_only unless --mode is explicitly supplied.
    # Read the durable mode from setup.yaml so data_anchored sessions actually
    # reach the data-fitting path and --data is not silently ignored.
    setup_path = Path(setup)
    if not setup_path.is_absolute():
        setup_path = BASE / setup_path

    try:
        setup_cfg = yaml.safe_load(setup_path.read_text(encoding="utf-8")) or {}
    except Exception as exc:
        raise RuntimeError(f"Cannot read MEDA setup.yaml: {setup_path}: {exc}") from exc

    mode = str(setup_cfg.get("mode", "constraint_only"))
    if mode not in {"data_anchored", "constraint_only"}:
        raise ValueError(
            f"Invalid MEDA mode in setup.yaml: {mode!r}. "
            "Expected 'data_anchored' or 'constraint_only'."
        )

    # main.py runs with cwd=MEDA, so all IMA paths must be absolute.
    setup_path = Path(setup)
    if not setup_path.is_absolute():
        setup_path = BASE / setup_path

    problem_path = Path(problem)
    if not problem_path.is_absolute():
        problem_path = BASE / problem_path

    output_path = Path(output)
    if not output_path.is_absolute():
        output_path = BASE / output_path

    data_path = None
    if data:
        data_path = Path(data)
        if not data_path.is_absolute():
            data_path = BASE / data_path

    command = [
        str(python),
        "skills/meda/scripts/main.py",
        "--mode", mode,
        "--setup", str(setup_path.resolve()),
        "--problem", str(problem_path.resolve()),
        "--output", str(output_path.resolve()),
    ]

    if data_path is not None:
        command += ["--data", str(data_path.resolve())]

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

    Creates a session and executes MEDA when concrete setup/problem/data
    inputs are supplied.
    """
    session = create_session(question)
    context = dict(context or {})

    (session / "research_request.json").write_text(
        json.dumps(
            {
                "source": "IMA",
                "question": question,
                "context": context,
                "created_at": datetime.now().isoformat(),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    payload = {
        "ok": True,
        "question": question,
        "session": str(session),
        "environment_ready": meda_environment_ready(),
        "status": status(),
        "executed": False,
        "context": context,
    }

    if not meda_environment_ready():
        payload["ok"] = False
        payload["error"] = "MEDA core environment is not ready"
        return payload

    setup = context.get("setup")
    problem = context.get("problem")
    data = context.get("data")

    if not setup or not problem:
        payload["ok"] = False
        payload["error"] = "MEDA requires setup and problem inputs"
        return payload

    setup_path = Path(setup)
    problem_path = Path(problem)

    if not setup_path.is_absolute():
        setup_path = BASE / setup_path
    if not problem_path.is_absolute():
        problem_path = BASE / problem_path

    if not setup_path.is_file():
        payload["ok"] = False
        payload["error"] = f"setup file not found: {setup_path}"
        return payload

    if not problem_path.is_file():
        payload["ok"] = False
        payload["error"] = f"problem file not found: {problem_path}"
        return payload

    data_path = None
    if data:
        data_path = Path(data)
        if not data_path.is_absolute():
            data_path = BASE / data_path

        if not data_path.is_file():
            payload["ok"] = False
            payload["error"] = f"data file not found: {data_path}"
            return payload

    output_value = context.get("output", "results.json")
    output_path = Path(output_value)

    if not output_path.is_absolute():
        output_path = session / output_path

    try:
        result = run_meda(
            setup=str(setup_path),
            problem=str(problem_path),
            output=str(output_path),
            data=str(data_path) if data_path else None,
        )
    except Exception as exc:
        payload["ok"] = False
        payload["error"] = "meda_execution_error"
        payload["exception"] = type(exc).__name__
        payload["message"] = str(exc)
        return payload

    payload["executed"] = True
    payload["returncode"] = result.returncode
    payload["stdout"] = result.stdout
    payload["stderr"] = result.stderr
    payload["output"] = str(output_path)

    if result.returncode == 0 and output_path.exists():
        payload["result"] = read_json(output_path)
    elif result.returncode != 0:
        payload["ok"] = False
        payload["error"] = "meda_process_failed"

    return payload
