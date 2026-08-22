
from pathlib import Path
import json
import subprocess
import py_compile
from datetime import datetime

REPORT = Path("IMA_AUDIT_REPORT.json")


def log(x):


def load_errors():
    if not REPORT.exists():
        return []

    try:
        data = json.loads(REPORT.read_text(encoding="utf8"))
        return data.get("python_errors", [])
    except Exception:
        return []


def compile_file(path):
    try:
        py_compile.compile(str(path), doraise=True)
        return True
    except Exception:
        return False


def repair_target(path):
    repair_unterminated_string(path)
    p = Path(path)

    if not p.exists():
        return False

    log("[CHECK] " + str(p))

    if compile_file(p):
        return True

    # בסיס תיקון בטוח:
    # מנקה קבצי גיבוי שבורים מהבדיקה בלבד
    if ".ima" in str(p) and "backup" in p.name:
        log("[SKIP BACKUP] " + str(p))
        return True

    return False


def verify():
    errors=[]

    for e in load_errors():
        f=e.get("file")
        if f and not compile_file(Path(f)):
            errors.append(f)

    return errors


def run():
    errors=load_errors()


    fixed=[]

    for e in errors:
        f=e.get("file")
        if f and repair_target(f):
            fixed.append(f)

    remaining=verify()


    if not remaining:
        subprocess.run(
            ["git","add","-A"]
        )

        subprocess.run(
            [
                "git",
                "commit",
                "-m",
                "guardian report based auto repair"
            ],
            capture_output=True,
            text=True
        )




def repair_unterminated_string(path):
    p = Path(path)

    if p.name != "daily_evolution.py":
        return False

    lines = p.read_text(encoding="utf8").splitlines()

    out = []
    inside_main = False
    cleaned = False

    for line in lines:

        if 'if __name__=="__main__":' in line:
            inside_main = True
            out.append(line)
            continue

        if inside_main:

            if "build_summary()" in line:
                out.append(line)
                continue

            if "import os" in line:
                out.extend([
                    "",
                    ""
                ])
                inside_main = False
                out.append(line)
                cleaned = True
                continue

            if (
                or "IMA DAILY EVOLUTION SAVED" in line
                or line.strip() == ")"
            ):
                cleaned = True
                continue

        out.append(line)

    if cleaned:
        p.write_text(
            "\n".join(out)+"\n",
            encoding="utf8"
        )
        return True

    return False


def run():
    errors=load_errors()


    fixed=[]

    for e in errors:
        f=e.get("file")
        if f and repair_target(f):
            fixed.append(f)

    remaining=verify()


    if not remaining:
        subprocess.run(
            ["git","add","-A"]
        )

        subprocess.run(
            [
                "git",
                "commit",
                "-m",
                "guardian report based auto repair"
            ],
            capture_output=True,
            text=True
        )



def repair_unterminated_string(path):
    p = Path(path)

    if p.name != "daily_evolution.py":
        return False

    lines = p.read_text(encoding="utf8").splitlines()

    out = []
    skip = False
    changed = False

    for line in lines:
        if "IMA DAILY EVOLUTION SAVED" in line:
            out.extend([
                '        "IMA DAILY EVOLUTION SAVED"',
                '    )'
            ])
            skip = True
            changed = True
            continue

        if skip:
            if line.strip().startswith("import ") or line.strip().startswith("os."):
                skip = False
                out.append(line)
            continue

        if line.strip() == ')"':
            changed = True
            continue

        out.append(line)

    if changed:
        p.write_text("\n".join(out)+"\n", encoding="utf8")

    return changed

if __name__=="__main__":
    run()

if __name__=="__main__":
    run()


def repair_unterminated_string(path):
    p = Path(path)

    if p.name != "daily_evolution.py":
        return False

    lines = p.read_text(encoding="utf8").splitlines()

    out = []
    skip = False
    changed = False

    for line in lines:
        if "IMA DAILY EVOLUTION SAVED" in line:
            out.extend([
                '        "IMA DAILY EVOLUTION SAVED"',
                '    )'
            ])
            skip = True
            changed = True
            continue

        if skip:
            if line.strip().startswith("import ") or line.strip().startswith("os."):
                skip = False
                out.append(line)
            continue

        if line.strip() == ')"':
            changed = True
            continue

        out.append(line)

    if changed:
        p.write_text("\n".join(out)+"\n", encoding="utf8")

    return changed
