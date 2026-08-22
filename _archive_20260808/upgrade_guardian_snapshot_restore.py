from pathlib import Path
import shutil
import py_compile

def guardian_restore_core():
    core = [
        "ima_guardian_watch.py",
        "ima_guardian_self_repair.py",
        "ima_guardian_master.py",
        "ima_guardian_controller.py"
    ]

    snap = Path(".ima/guardian/snapshots/core")

    for f in core:
        target = Path(f)

        try:
            py_compile.compile(str(target), doraise=True)
        except Exception:
            backup = snap / f

            if backup.exists():
                shutil.copy2(backup, target)

                try:
                    py_compile.compile(str(target), doraise=True)
                except Exception:

if __name__ == "__main__":
    guardian_restore_core()
