#!/data/data/com.termux/files/usr/bin/bash
set -e

echo "=== CONNECT WATCHDOG TO BOOT ==="

cp IMA_START.py IMA_START.py.before_watchdog_boot

python3 - <<'PY'
from pathlib import Path

p=Path("IMA_START.py")
s=p.read_text()

block='''
def verify_watchdog():
    import subprocess
    import sys

    r=subprocess.run(
        ["python3","kernel/runtime/CANONICAL/IMA_WATCHDOG.py"],
        capture_output=True,
        text=True
    )

    print(r.stdout)

    if r.returncode != 0:
        print("[FAIL] WATCHDOG BLOCKED BOOT")
        sys.exit(1)

    print("[OK] WATCHDOG PASSED")

'''

if "def verify_watchdog" not in s:
    marker="ROOT = Path(__file__).resolve().parent"
    s=s.replace(marker, block+"\n"+marker, 1)

if "verify_watchdog()" not in s:
    marker='print("=== IMA ONLINE START ===")'
    s=s.replace(
        marker,
        "verify_watchdog()\n\n"+marker,
        1
    )

p.write_text(s)

print("[OK] watchdog connected to IMA_START")
PY


echo ""
echo "=== VERIFY FULL BOOT ==="

python3 IMA_START.py

echo ""
echo "=== WATCHDOG BOOT LOCK ACTIVE ==="
