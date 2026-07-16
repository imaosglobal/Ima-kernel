from pathlib import Path
import subprocess
import json
import re

REPORT = Path("IMA_AUDIT_REPORT.json")


def run(cmd):
    return subprocess.run(
        cmd,
        shell=True,
        text=True,
        capture_output=True
    )


def find_errors():

    if not REPORT.exists():
        return []

    try:
        data=json.loads(
            REPORT.read_text(encoding="utf8")
        )
    except:
        return []

    errors=[]

    for k,v in data.items():
        if isinstance(v,list):
            errors.extend(v)

    return errors


def compile_scan():

    result = run(
        "python3 -m compileall -q ."
    )

    if result.returncode:
        return result.stderr.splitlines()

    return []


def repair_file(path):

    p=Path(path)

    if not p.exists():
        return

    text=p.read_text(
        encoding="utf8",
        errors="ignore"
    )

    changed=False


    # תיקון import חסר נפוץ
    if "subprocess.run" in text:
        if "import subprocess" not in text:
            text="import subprocess\n"+text
            changed=True


    if "json.dumps" in text:
        if "import json" not in text:
            text="import json\n"+text
            changed=True


    if changed:
        p.write_text(
            text,
            encoding="utf8"
        )

        print("[FIXED]",p)


def discover_python_files():

    return [
        str(x)
        for x in Path(".").rglob("*.py")
        if ".git" not in str(x)
        and ".ima/backups" not in str(x)
        and "__pycache__" not in str(x)
    ]


def repair():

    print("=== SELF REPAIR ENGINE ===")

    files=discover_python_files()

    before=compile_scan()

    print(
        "[ERRORS BEFORE]",
        len(before)
    )


    for f in files:
        repair_file(f)


    after=compile_scan()


    print(
        "[ERRORS AFTER]",
        len(after)
    )


    return len(after)==0


if __name__=="__main__":
    repair()
