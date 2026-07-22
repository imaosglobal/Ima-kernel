from pathlib import Path
import subprocess
import sys
import time
import json

ROOT = Path(__file__).parent
os.chdir(ROOT) if False else None

print("=== IMA MANAGED START ===")

steps = [
    (
        "MANAGEMENT_LAYER",
        [
            sys.executable,
            ".ima/MANAGEMENT/boot_management_check.py"
        ]
    ),
    (
        "CANONICAL_SINGLE_ENTRY",
        [
            sys.executable,
            ".ima/CANONICAL_AUTHORITY/entry/IMA_START_SINGLE_ENTRY.py"
        ]
    )
]

failed = []

for name, command in steps:
    print()
    print(">>>", name)

    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True
    )

    print(result.stdout)

    if result.stderr:
        print(result.stderr)

    if result.returncode != 0:
        failed.append(name)
        break

report = {
    "time": time.time(),
    "entry": "IMA_MANAGED_START",
    "status": "READY" if not failed else "FAILED",
    "failed": failed
}

out = ROOT / ".ima/MANAGEMENT/managed_start_report.json"
out.write_text(json.dumps(report, indent=2))

print()
print("=== MANAGED START RESULT ===")
print(report["status"])
print("REPORT:", out)

if failed:
    sys.exit(1)
