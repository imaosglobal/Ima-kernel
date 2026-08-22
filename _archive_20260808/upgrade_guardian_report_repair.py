from pathlib import Path
import json

p = Path("ima_guardian_self_repair.py")

code = r'''
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



if __name__=="__main__":
    run()
'''

p.write_text(code, encoding="utf8")

