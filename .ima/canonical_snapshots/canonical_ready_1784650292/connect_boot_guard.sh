#!/data/data/com.termux/files/usr/bin/bash
set -e

echo "=== CONNECT CANONICAL BOOT GUARD ==="

cp IMA_START.py IMA_START.py.before_boot_guard

python3 - <<'PY'
from pathlib import Path

p=Path("IMA_START.py")
s=p.read_text()

guard='''

def verify_canonical_boot():
    import subprocess
    import sys

    result=subprocess.run(
        ["python3",".ima/governance/../verify_canonical_root.py"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("[FAIL] CANONICAL ROOT BLOCKED")
        print(result.stdout)
        print(result.stderr)
        sys.exit(1)

    print("[OK] CANONICAL ROOT PASSED")

'''

if "def verify_canonical_boot" not in s:
    marker="ROOT = Path(__file__).resolve().parent"
    s=s.replace(marker,guard+"\n"+marker,1)

if "verify_canonical_boot()" not in s:
    marker="print(\"=== IMA ONLINE START ===\")"
    s=s.replace(marker,"verify_canonical_boot()\n\n"+marker,1)

p.write_text(s)

print("[OK] IMA_START patched")
PY


echo ""
echo "=== VERIFY BOOT ==="

python3 IMA_START.py

echo ""
echo "=== BOOT GUARD ACTIVE ==="
