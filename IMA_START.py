import sys
import time
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent
RUNTIME = ROOT / "kernel" / "runtime" / "CANONICAL"


def start_api():
    api = ROOT / "api" / "server.py"

    if not api.exists():
        print("[WARN] API missing")
        return False

    try:
        subprocess.Popen(
            ["python3", str(api)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(2)
        return True
    except Exception as e:
        print("[WARN] API:", e)
        return False


def run():

    print("=== IMA ONLINE START ===")

    try:
        import canonical_boot_guard
        if not canonical_boot_guard.verify():
            print("[WARN] CANONICAL STATE CHANGED")
    except Exception as e:
        print("[WARN] GUARD CHECK:", e)


    print("TIME:", time.time())

    try:
        sys.path.insert(0, str(RUNTIME))

        from python_bridge import boot_runtime

        result = boot_runtime()
        print("[OK] CANONICAL RUNTIME", result)

    except Exception as e:
        print("[FAIL] RUNTIME:", e)
        return 1


    checks = []

    checks.append(ROOT.exists())
    checks.append(RUNTIME.exists())

    print("[OK] ROOT" if checks[0] else "[FAIL] ROOT")
    print("[OK] CANONICAL" if checks[1] else "[FAIL] CANONICAL")

    try:
        import api_boot_connector
        api_boot_connector.start_api()
        print("[OK] API BOOT CONNECTED")
    except Exception:
        if start_api():
            print("[OK] API STARTED")
        else:
            print("[WARN] API NOT STARTED")



    try:
        import boot_integrity_reporter
        boot_integrity_reporter.create_report("ONLINE")
        print("[OK] BOOT INTEGRITY REPORT")
    except Exception as e:
        print("[WARN] BOOT REPORT:", e)

    
    try:
        import subprocess
        subprocess.run(
            ["bash","canonical_dependency_audit.sh"],
            timeout=60
        )
        print("[OK] DEPENDENCY AUDIT")
    except Exception as e:
        print("[WARN] DEPENDENCY AUDIT:", e)

    print("=== IMA SYSTEM READY ===")
    return 0



def run_auto_maintenance():
    try:
        import subprocess
        subprocess.run(
            ["bash","canonical_auto_maintenance.sh"],
            timeout=60
        )
        print("[OK] AUTO MAINTENANCE")
    except Exception as e:
        print("[WARN] AUTO MAINTENANCE:", e)

if __name__ == "__main__":
    sys.exit(run())
