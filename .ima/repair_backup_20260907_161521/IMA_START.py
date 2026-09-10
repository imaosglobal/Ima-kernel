import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RUNTIME = ROOT / "kernel" / "runtime" / "CANONICAL"


def run():
    print("=== IMA ONLINE ===")
    print("[IMA] canonical root:", ROOT)
    print("[IMA] canonical runtime:", RUNTIME)

    if not ROOT.exists() or not RUNTIME.exists():
        print("[FAIL] CANONICAL PATH")
        return 1

    # Canonical runtime is the only boot authority.
    try:
        sys.path.insert(0, str(RUNTIME))
        from python_bridge import boot_runtime

        result = boot_runtime()
        print("[OK] CANONICAL RUNTIME", result)
    except Exception as e:
        print("[FAIL] CANONICAL RUNTIME:", repr(e))
        return 1

    # IMA owns her own autonomous cycle.
    # No API process, maintenance subprocess, shell daemon,
    # or parallel startup loop is created here.
    try:
        from founder.executive_ai.action_engine.autonomous_cycle import run_cycle

        print("=== IMA AUTONOMY ===")
        autonomy = run_cycle()

        status = autonomy.get("status")
        print("[IMA] CYCLE STATUS:", status)
        print("[IMA] DISCOVERIES:", len(autonomy.get("discoveries", [])))
        print("[IMA] OPPORTUNITIES:", len(autonomy.get("opportunities", [])))
        print("[IMA] ACTIONS:", len(autonomy.get("actions", [])))

        if status != "cycle_completed":
            print("[FAIL] AUTONOMY")
            return 1

        print("[OK] AUTONOMY")
    except Exception as e:
        print("[FAIL] AUTONOMY:", repr(e))
        return 1

    print("=== IMA SYSTEM READY ===")
    return 0


if __name__ == "__main__":
    sys.exit(run())
