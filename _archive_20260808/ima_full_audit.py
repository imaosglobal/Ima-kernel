
EXCLUDED_DIRS = {
    ".ima/backups",
    ".ima/archive",
    "archive",
    "snapshots",
    "__pycache__",
}

def should_skip(path):
    s = str(path)
    return any(x in s for x in EXCLUDED_DIRS) or "broken_backup" in s or "learning_backup" in s

from pathlib import Path
import ast
import json
import hashlib
import subprocess
import sys
from datetime import datetime

ROOT = Path(".")
REPORT = Path("IMA_AUDIT_REPORT.json")

report = {
    "time": str(datetime.now()),
    "root": str(ROOT.resolve()),
    "python_errors": [],
    "imports": [],
    "duplicates": {},
    "files": {},
    "stats": {}
}

EXCLUDED = [
    ".ima/broken_runtime_backup.py",
    ".ima/backups",
    ".ima/archive",
    "archive",
    "snapshots",
    ".ima/backups",
    ".ima/archive",
    "archive",
    "snapshots",
    "__pycache__",
    "learning_backup",
    "broken_backup",
]

py_files = [
    x for x in ROOT.rglob("*.py")
    if not any(e in str(x) for e in EXCLUDED)
]

report["stats"]["python_files"] = len(py_files)

print("[1] scanning python files:", len(py_files))

for p in py_files:
    try:
        data = p.read_bytes()
        h = hashlib.sha256(data).hexdigest()

        report["files"][str(p)] = {
            "size": len(data),
            "sha256": h
        }

        try:
            ast.parse(data.decode("utf8"))
        except Exception as e:
            report["python_errors"].append({
                "file": str(p),
                "error": str(e)
            })

    except Exception as e:
        report["python_errors"].append({
            "file": str(p),
            "error": str(e)
        })


print("[2] checking duplicate files")

hash_map = {}

for f, info in report["files"].items():
    hash_map.setdefault(info["sha256"], []).append(f)

for h, files in hash_map.items():
    if len(files) > 1:
        report["duplicates"][h] = files


print("[3] checking imports")

for p in py_files:
    try:
        tree = ast.parse(p.read_text(errors="ignore"))

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names:
                    report["imports"].append({
                        "file": str(p),
                        "import": n.name
                    })

            if isinstance(node, ast.ImportFrom):
                report["imports"].append({
                    "file": str(p),
                    "import": node.module
                })

    except:
        pass


print("[4] compiling check")

for p in py_files:
    try:
        r = subprocess.run(
            [sys.executable, "-m", "py_compile", str(p)],
            capture_output=True,
            text=True
        )

        if r.returncode != 0:
            report["python_errors"].append({
                "file": str(p),
                "compile": r.stderr[-500:]
            })

    except Exception as e:
        pass


report["stats"]["syntax_errors"] = len(report["python_errors"])
report["stats"]["duplicate_groups"] = len(report["duplicates"])

REPORT.write_text(
    json.dumps(report,indent=2,ensure_ascii=False),
    encoding="utf8"
)

print()
print("=== IMA AUDIT COMPLETE ===")
print("Python files:", report["stats"]["python_files"])
print("Syntax errors:", report["stats"]["syntax_errors"])
print("Duplicate groups:", report["stats"]["duplicate_groups"])
print("Report:", REPORT)
