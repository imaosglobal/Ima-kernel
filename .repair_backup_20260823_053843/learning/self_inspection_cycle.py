from pathlib import Path
from datetime import datetime
import json

from learning.autonomy_engine import run_autonomy
from learning.lesson_retrieval import retrieve_relevant_lessons


ROOT = Path(".")


IGNORED_DIRS = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "node_modules",
}


def scan_repository(root=ROOT):
    """
    Read-only repository inspection.

    Scans Python files and directories.
    Does not modify files.
    Does not execute discovered code.
    """

    files = []
    directories = []
    python_files = []

    for path in root.rglob("*"):

        if any(
            ignored in path.parts
            for ignored in IGNORED_DIRS
        ):
            continue

        if path.is_dir():
            directories.append(str(path))

        elif path.is_file():
            files.append(str(path))

            if path.suffix == ".py":
                python_files.append(path)

    modules = []

    for path in python_files:

        try:
            text = path.read_text(
                encoding="utf-8",
                errors="ignore",
            )

            lines = text.splitlines()

            functions = [
                line.strip()
                for line in lines
                if line.strip().startswith("def ")
            ]

            classes = [
                line.strip()
                for line in lines
                if line.strip().startswith("class ")
            ]

            modules.append({
                "path": str(path),
                "size": len(text),
                "lines": len(lines),
                "functions": functions,
                "classes": classes,
            })

        except Exception as exc:

            modules.append({
                "path": str(path),
                "error": str(exc),
            })

    return {
        "root": str(root.resolve()),
        "directories": directories,
        "files": files,
        "python_files": python_files,
        "modules": modules,
        "status": "repository_scanned",
        "execution": "disabled",
    }


def build_observations(scan):
    """
    Converts repository inspection into explicit observations.
    """

    observations = []

    module_count = len(scan["modules"])
    file_count = len(scan["files"])
    directory_count = len(scan["directories"])

    observations.append(
        f"repository contains {file_count} files"
    )

    observations.append(
        f"repository contains {directory_count} directories"
    )

    observations.append(
        f"repository contains {module_count} Python modules"
    )

    for module in scan["modules"]:

        if "error" in module:
            observations.append(
                f"module inspection failed: {module['path']}"
            )
            continue

        if not module.get("functions"):
            observations.append(
                f"module has no detected functions: "
                f"{module['path']}"
            )

        if not module.get("classes"):
            observations.append(
                f"module has no detected classes: "
                f"{module['path']}"
            )

    return observations


def run_self_inspection():


    # 1. READ-ONLY REPOSITORY SCAN
    scan = scan_repository()

    observations = build_observations(scan)

    context = {
        "observations": observations,
        "goals": [
            "understand repository structure",
            "identify capability gaps",
            "continue safe learning",
        ],
        "constraints": [
            "read-only inspection",
            "no autonomous execution",
            "no self-modification",
        ],
    }

    # 2. RETRIEVE PREVIOUS LESSONS
    lessons = retrieve_relevant_lessons(context)

    # 3. REASON -> PLAN -> EVALUATE -> FEEDBACK -> LESSON
    autonomy = run_autonomy(context)

    result = {
        "timestamp": str(datetime.now()),
        "scan": scan,
        "observations": observations,
        "retrieved_lessons": lessons,
        "autonomy": autonomy,
        "execution": "disabled",
        "self_modification": "disabled",
        "status": "self_inspection_cycle_completed",
    }

        "FILES:",
        len(scan["files"])
    )

        "DIRECTORIES:",
        len(scan["directories"])
    )

        "PYTHON MODULES:",
        len(scan["python_files"])
    )

        len(lessons.get("matches", []))
    )

        autonomy.get("status")
    )

        result["execution"]
    )

        result["self_modification"]
    )


    return result


if __name__ == "__main__":
    run_self_inspection()
