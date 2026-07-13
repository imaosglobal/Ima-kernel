#!/usr/bin/env python3

"""
IMA START - Canonical Entry Point

Flow:

BOOT
 |
GATE
 |
BRAIN
 |
ORCHESTRATOR
 |
LEARNING
 |
MEMORY
 |
SAFETY
"""

from pathlib import Path
import json
import time
import sys





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


ROOT = Path(__file__).resolve().parent

RUNTIME = ROOT / "kernel" / "runtime" / "CANONICAL"
sys.path.insert(0, str(RUNTIME))

BRAIN = ROOT / "learning" / "meta_orchestrator.py"
CONNECTOR = ROOT / "learning" / "module_registry.py"

GOVERNANCE = ROOT / ".ima" / "governance"

REGISTRY = GOVERNANCE / "brain_registry.json"


def status(name, ok, detail=""):
    symbol = "OK" if ok else "FAIL"
    print(f"[{symbol}] {name}", detail)


def check_files():
    checks = {
        "ROOT": ROOT.exists(),
        "BRAIN": BRAIN.exists(),
        "CONNECTOR": CONNECTOR.exists(),
        "GOVERNANCE": GOVERNANCE.exists(),
        "REGISTRY": REGISTRY.exists(),
    }

    for k, v in checks.items():
        status(k, v)

    return all(checks.values())


def check_brain_lock():
    if not REGISTRY.exists():
        status("BRAIN LOCK", False, "missing registry")
        return False

    data = json.loads(REGISTRY.read_text(encoding="utf-8"))

    locked = (
        data.get("state") == "LOCKED"
        and data.get("brain") == "learning/meta_orchestrator.py"
    )

    status(
        "BRAIN LOCK",
        locked,
        data.get("brain", "")
    )

    return locked


def check_learning():
    try:
        from learning.meta_orchestrator import run_meta_analysis

        result = run_meta_analysis()

        status(
            "LEARNING ENGINE",
            True,
            f"capabilities={result.get('capabilities')}"
        )

        return True

    except Exception as e:
        status("LEARNING ENGINE", False, str(e))
        return False


def check_memory():
    files = [
        ".ima/memory.json",
        ".ima/ledger.jsonl",
        ".ima/personality.json",
        ".ima/voice.json",
    ]

    ok = True

    for f in files:
        exists = (ROOT / f).exists()
        status("MEMORY " + f, exists)
        ok = ok and exists

    return ok



def check_runtime():
    try:
        from python_bridge import boot_runtime
        result = boot_runtime()

        ok = result.get("status") == "ONLINE"

        status(
            "CANONICAL RUNTIME",
            ok,
            str(result)
        )

        return ok

    except Exception as e:
        status(
            "CANONICAL RUNTIME",
            False,
            str(e)
        )
        return False


def run():

    print()
    verify_watchdog()

    print("=== IMA ONLINE START ===")
    print("TIME:", time.time())
    print()

    results = [
        check_runtime(),
        check_files(),
        check_brain_lock(),
        check_learning(),
        check_memory(),
    ]

    print()
    if all(results):
        print("=== IMA SYSTEM READY ===")
        return 0

    print("=== IMA SYSTEM FAILED ===")
    return 1


if __name__ == "__main__":
    sys.exit(run())
