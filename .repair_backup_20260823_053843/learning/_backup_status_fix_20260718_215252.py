from pathlib import Path
from datetime import datetime
import ast
import json
import shutil
import difflib
import sys

ROOT = Path(".")
LEARNING_DIR = ROOT / "learning"
REPORT_DIR = LEARNING_DIR / "self_improvement_reports"
BACKUP_DIR = LEARNING_DIR / "self_improvement_backups"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

ALLOWLIST = {
    "learning/reasoning_engine.py",
    "learning/planning_engine.py",
    "learning/evaluation_engine.py",
    "learning/plan_feedback.py",
    "learning/lesson_memory.py",
    "learning/lesson_retrieval.py",
}


def scan_repository():
    files = []
    python_modules = []

    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue

        if any(
            part in {".git", "__pycache__", ".venv", "venv"}
            for part in path.parts
        ):
            continue

        files.append(str(path))

        if path.suffix == ".py":
            python_modules.append(str(path))

    return {
        "files": len(files),
        "python_modules": len(python_modules),
        "directories": sum(
            1 for p in ROOT.rglob("*")
            if p.is_dir()
        ),
        "python_files": python_modules,
    }


def inspect_python_file(path):
    result = {
        "path": str(path),
        "syntax_valid": False,
        "functions": [],
        "classes": [],
        "errors": [],
    }

    try:
        text = path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        tree = ast.parse(text)

        result["syntax_valid"] = True

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                result["functions"].append(node.name)

            elif isinstance(node, ast.AsyncFunctionDef):
                result["functions"].append(node.name)

            elif isinstance(node, ast.ClassDef):
                result["classes"].append(node.name)

    except Exception as exc:
        result["errors"].append(str(exc))

    return result


def inspect_repository(scan):
    return [
        inspect_python_file(Path(filename))
        for filename in scan["python_files"]
    ]


def find_gaps(inspections):
    gaps = []

    for item in inspections:
        if not item["syntax_valid"]:
            gaps.append({
                "type": "syntax_error",
                "file": item["path"],
                "reason": "Python syntax validation failed",
            })

    return gaps


def build_improvement_plan(gaps):
    steps = []

    for index, gap in enumerate(gaps, 1):
        steps.append({
            "step": index,
            "file": gap["file"],
            "action": "review",
            "reason": gap["reason"],
            "status": "planned",
        })

    return {
        "steps": steps,
        "status": "planned",
        "execution": "disabled",
    }


def evaluate_plan(plan):
    valid_steps = [
        step
        for step in plan.get("steps", [])
        if (
            isinstance(step, dict)
            and step.get("file")
            and step.get("action")
        )
    ]

    allowlist_pass = all(
        step["file"] in ALLOWLIST
        for step in valid_steps
    )

    return {
        "valid_steps": len(valid_steps),
        "allowlist_pass": allowlist_pass,
        "execution_disabled": True,
        "score": 1.0 if allowlist_pass else 0.0,
        "status": "plan_evaluated",
    }


def generate_patch_proposal(path):
    original = path.read_text(
        encoding="utf-8",
        errors="ignore",
    )

    marker = "# IMA_SELF_IMPROVEMENT_MARKER"

    if marker in original:
        return {
            "file": str(path),
            "changed": False,
            "reason": "marker already exists",
            "original": original,
            "proposed": original,
            "diff": "",
        }

    proposed = (
        original.rstrip()
        + "\n\n"
        + marker
        + "\n"
    )

    diff = "".join(
        difflib.unified_diff(
            original.splitlines(True),
            proposed.splitlines(True),
            fromfile=str(path),
            tofile=str(path) + ".proposed",
        )
    )

    return {
        "file": str(path),
        "changed": True,
        "original": original,
        "proposed": proposed,
        "diff": diff,
    }


def validate_patch(proposal):
    if not proposal.get("changed"):
        return {
            "valid": True,
            "status": "no_change_required",
        }

    try:
        ast.parse(proposal["proposed"])

        return {
            "valid": True,
            "status": "patch_syntax_valid",
        }

    except Exception as exc:
        return {
            "valid": False,
            "status": "patch_syntax_invalid",
            "error": str(exc),
        }


def apply_patch(proposal):
    path = Path(proposal["file"])

    if str(path) not in ALLOWLIST:
        return {
            "status": "blocked",
            "reason": "file not in allowlist",
        }

    backup_path = (
        BACKUP_DIR
        / (
            path.name
            + "."
            + datetime.now().strftime("%Y%m%d_%H%M%S")
            + ".bak"
        )
    )

    shutil.copy2(path, backup_path)

    path.write_text(
        proposal["proposed"],
        encoding="utf-8",
    )

    return {
        "status": "applied",
        "file": str(path),
        "backup": str(backup_path),
    }


def run_self_improvement(apply=False):

    scan = scan_repository()


    inspections = inspect_repository(scan)
    gaps = find_gaps(inspections)


    plan = build_improvement_plan(gaps)
    evaluation = evaluate_plan(plan)


        json.dumps(
            evaluation,
            indent=2,
            ensure_ascii=False,
        )
    )

    proposals = []

    for step in plan["steps"]:
        path = Path(step["file"])

        if str(path) not in ALLOWLIST:
            continue

        proposal = generate_patch_proposal(path)
        validation = validate_patch(proposal)

        proposals.append({
            "proposal": proposal,
            "validation": validation,
        })

    applied = []

    apply_allowed = (
        apply
        and evaluation.get("score") == 1.0
        and evaluation.get("allowlist_pass") is True
        and evaluation.get("execution_disabled") is True
    )

    if apply and not apply_allowed:

    elif apply_allowed:

        for item in proposals:
            proposal = item["proposal"]
            validation = item["validation"]

            if not validation["valid"]:
                    "SKIPPED INVALID PATCH:",
                    proposal["file"],
                )
                continue

            applied.append(
                apply_patch(proposal)
            )

    else:

    report = {
        "timestamp": str(datetime.now()),
        "scan": {
            "files": scan["files"],
            "directories": scan["directories"],
            "python_modules": scan["python_modules"],
        },
        "gaps": gaps,
        "plan": plan,
        "evaluation": evaluation,
        "proposals": [
            {
                "file": item["proposal"]["file"],
                "changed": item["proposal"].get("changed"),
                "validation": item["validation"],
                "diff": item["proposal"].get("diff", ""),
            }
            for item in proposals
        ],
        "applied": applied,
        "execution": "enabled" if apply_allowed else "disabled",
        "self_modification": "enabled" if apply_allowed else "disabled",
        "status": "self_improvement_cycle_completed",
    }

    report_path = (
        REPORT_DIR
        / (
            "report_"
            + datetime.now().strftime("%Y%m%d_%H%M%S")
            + ".json"
        )
    )

    report_path.write_text(
        json.dumps(
            report,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

        "EXECUTION:",
        "enabled" if apply else "disabled",
    )
        "SELF-MODIFICATION:",
        "enabled" if apply else "disabled",
    )

    return report


if __name__ == "__main__":
    run_self_improvement(
        apply="--apply" in sys.argv
    )
