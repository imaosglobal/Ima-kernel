import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
REGISTRY = ROOT / ".ima/CANONICAL_AUTHORITY/governance/CANONICAL_REGISTRY.json"

def fail(name, detail=""):
    print(f"FAIL {name}")
    if detail:
        print(detail[-500:])
    raise SystemExit(1)

# 1. Canonical registry + hashes
try:
    registry = json.loads(REGISTRY.read_text())
    for item in registry["allowed_components"]:
        path = ROOT / item["file"]
        if not path.is_file():
            fail("CANONICAL_HASH", f"MISSING {path}")

        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != item["sha256"]:
            fail(
                "CANONICAL_HASH",
                f"MISMATCH {path}\nEXPECTED {item['sha256']}\nACTUAL   {actual}",
            )

    print("PASS CANONICAL_HASH")
except Exception as e:
    fail("CANONICAL_HASH", str(e))

# 2. Active compile
compile_targets = [
    ROOT / "kernel",
    ROOT / ".ima/CANONICAL_AUTHORITY",
    ROOT / ".ima/agi_evolution",
]

r = subprocess.run(
    [sys.executable, "-m", "compileall", "-q", *map(str, compile_targets)],
    cwd=ROOT,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
)

if r.returncode != 0:
    fail("ACTIVE_COMPILE", r.stderr)

print("PASS ACTIVE_COMPILE")

# 3. HTTP adapter
r = subprocess.run(
    [
        sys.executable,
        str(ROOT / ".ima/CANONICAL_AUTHORITY/entry/IMA_HTTP_ADAPTER_SELFTEST.py"),
    ],
    cwd=ROOT,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
)

if r.returncode != 0:
    fail("HTTP_ADAPTER", r.stderr)

print("PASS HTTP_ADAPTER")

# 4. Canonical boot
r = subprocess.run(
    [
        sys.executable,
        str(ROOT / ".ima/CANONICAL_AUTHORITY/entry/IMA_START_SINGLE_ENTRY.py"),
    ],
    cwd=ROOT,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
)

if r.returncode != 0:
    fail("CANONICAL_BOOT", r.stderr)

print("PASS CANONICAL_BOOT")
print("IMA_VALIDATION_OK")
