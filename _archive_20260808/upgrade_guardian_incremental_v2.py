from pathlib import Path

p = Path("ima_guardian_watch.py")

text = p.read_text(encoding="utf8")

if "guardian_incremental_check" not in text:

    addition = r'''

def guardian_incremental_check():
    import subprocess
    import py_compile


    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD"],
        capture_output=True,
        text=True
    )

    files = [
        x.strip()
        for x in result.stdout.splitlines()
        if x.endswith(".py")
    ]


    errors=[]

    for f in files:
        try:
            py_compile.compile(
                f,
                doraise=True
            )

        except Exception as e:
            errors.append(f)

    if errors:
        for e in errors:

        subprocess.run(
            ["python3","ima_guardian_self_repair.py"]
        )

    return len(errors)==0

'''

    text += addition

p.write_text(text, encoding="utf8")

