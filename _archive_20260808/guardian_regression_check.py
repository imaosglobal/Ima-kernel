from pathlib import Path
import subprocess

files = [
    "ima_guardian_watch.py",
    "ima_guardian_self_repair.py",
    "ima_guardian_master.py",
    "ima_guardian_controller.py",
]


failed = []

for f in files:
    if not Path(f).exists():
        failed.append(f)
        continue

    r = subprocess.run(
        ["python3", "-m", "py_compile", f],
        capture_output=True,
        text=True
    )

    if r.returncode != 0:
        failed.append(f)
    else:

if failed:
    raise SystemExit(1)

