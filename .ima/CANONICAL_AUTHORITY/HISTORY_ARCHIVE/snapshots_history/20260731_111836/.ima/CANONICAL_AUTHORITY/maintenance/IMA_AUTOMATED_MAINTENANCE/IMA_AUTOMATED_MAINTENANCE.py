from pathlib import Path
import subprocess
import sys

ROOT = Path.home() / "ima_kernel"

CHECKS = [
    (
        "BOOT",
        [
            sys.executable,
            str(ROOT / ".ima/CANONICAL_AUTHORITY/entry/IMA_START_SINGLE_ENTRY.py"),
        ],
    ),
    (
        "ACTIVE_COMPILE",
        [
            sys.executable,
            "-m",
            "compileall",
            "-q",
            str(ROOT / "kernel"),
            str(ROOT / ".ima/CANONICAL_AUTHORITY"),
            str(ROOT / ".ima/agi_evolution"),
        ],
    ),
]

for name, cmd in CHECKS:
    result = subprocess.run(
        cmd,
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.returncode != 0:
        print(f"[FAIL] {name}")
        print(result.stderr.splitlines()[-1:] or ["unknown error"])
        raise SystemExit(1)

    print(f"[OK] {name}")

print("[OK] SYSTEM READY")
