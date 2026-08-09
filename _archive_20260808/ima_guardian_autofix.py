from pathlib import Path
import subprocess
import py_compile

ROOT = Path(".")

REPAIRS = [
    "repair_source_manager.py",
    "repair_knowledge_pipeline.py",
    "repair_knowledge_gate.py",
    "repair_orchestrator_logic.py",
    "upgrade_knowledge_relevance.py",
]

def run_file(name):
    p = ROOT / name

    if not p.exists():
        print("[SKIP]", name)
        return

    print("[RUN]", name)

    r = subprocess.run(
        ["python3", str(p)],
        text=True,
        capture_output=True
    )

    if r.returncode:
        print("[FAIL]", name)
        print(r.stderr[-300:])
    else:
        print("[OK]", name)


def validate_core():

    targets = [
        "learning/source_manager.py",
        "learning/knowledge_core",
    ]

    for t in targets:
        p = Path(t)

        if p.is_file():
            try:
                py_compile.compile(
                    str(p),
                    doraise=True
                )
                print("[COMPILE OK]", p)

            except Exception as e:
                print("[COMPILE FAIL]", p, e)


def run():

    print("=== IMA GUARDIAN AUTOFIX ===")

    for r in REPAIRS:
        run_file(r)

    validate_core()

    print("=== AUTOFIX COMPLETE ===")


if __name__ == "__main__":
    run()
