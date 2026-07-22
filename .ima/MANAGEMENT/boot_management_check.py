from pathlib import Path
import subprocess
import sys

check = Path(".ima/MANAGEMENT/verify_management.py")

result = subprocess.run(
    [sys.executable, str(check)],
    capture_output=True,
    text=True
)

print(result.stdout)

if result.returncode != 0 or "STATUS: READY" not in result.stdout:
    print("MANAGEMENT_CHECK_FAILED")
    sys.exit(1)

print("MANAGEMENT_CHECK_OK")
