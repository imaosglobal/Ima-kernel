from pathlib import Path

p = Path("ima_guardian_watch.py")
text = p.read_text(encoding="utf8")

if "def incremental_cycle" not in text:

    add = r'''

def incremental_cycle():

    changed = smart_diff()

    print("=== SMART INCREMENTAL CYCLE ===")
    print("[CHANGED]", len(changed))

    if not changed:
        print("[OK] nothing changed")
        return

    python_changed = [
        x for x in changed
        if x.endswith(".py")
    ]

    if len(python_changed) <= 5:

        import subprocess

        for f in python_changed:
            print("[CHECK]", f)

            subprocess.run(
                [
                    "python3",
                    "-m",
                    "py_compile",
                    f
                ]
            )

    else:
        print("[FULL AUDIT REQUIRED]")

        import subprocess

        subprocess.run(
            [
                "python3",
                "ima_guardian_master.py"
            ]
        )

    update_smart_state()

'''

    text = text.replace(
        "def run_cycle():",
        add + "\ndef run_cycle():"
    )

p.write_text(text, encoding="utf8")

print("[OK] incremental guardian added")
