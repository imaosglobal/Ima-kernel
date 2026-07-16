from pathlib import Path

p = Path("ima_guardian_watch.py")

text = p.read_text(encoding="utf8")

if "guardian_incremental_check" not in text:

    addition = r'''

def guardian_incremental_check():
    import subprocess
    import py_compile

    print("=== GUARDIAN INCREMENTAL CHECK ===")

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

    print("[CHANGED PYTHON]", len(files))

    errors=[]

    for f in files:
        try:
            py_compile.compile(
                f,
                doraise=True
            )
            print("[OK]", f)

        except Exception as e:
            print("[FAIL]", f)
            errors.append(f)

    if errors:
        print("[REPAIR TARGETS]")
        for e in errors:
            print(e)

        subprocess.run(
            ["python3","ima_guardian_self_repair.py"]
        )

    return len(errors)==0

'''

    text += addition

p.write_text(text, encoding="utf8")

print("[OK] incremental guardian v2 added")
