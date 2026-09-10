import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RUNTIME = ROOT / "kernel" / "runtime" / "CANONICAL"
if str(RUNTIME) not in sys.path:
    sys.path.insert(0, str(RUNTIME))


def run():
    print("=== IMA CANONICAL START ===")
    print("[IMA] canonical root:", ROOT)

    if not RUNTIME.exists():
        print("[FAIL] CANONICAL RUNTIME")
        return 1

    # 1. Vision is loaded by the canonical runtime.
    try:
        from python_bridge import boot_runtime

        runtime = boot_runtime()

        print("[OK] CANONICAL RUNTIME")
        vision = runtime.get("canonical_vision")

        if not vision:
            print("[FAIL] VISION AUTHORITY")
            return 1

        print("[OK] VISION AUTHORITY")
        print("[IMA] VISION:", vision["path"])

    except Exception as e:
        print("[FAIL] CANONICAL RUNTIME:", repr(e))
        return 1

    # 2. One canonical autonomous cycle.
    try:
        from founder.executive_ai.action_engine.autonomous_cycle import run_cycle

        print("=== IMA AUTONOMY ===")
        autonomy = run_cycle()

        status = autonomy.get("status")

        print("[IMA] CYCLE STATUS:", status)
        print("[IMA] DISCOVERIES:",
              len(autonomy.get("discoveries", [])))
        print("[IMA] OPPORTUNITIES:",
              len(autonomy.get("opportunities", [])))
        print("[IMA] ACTIONS:",
              len(autonomy.get("actions", [])))

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
    sys.path.insert(0, str(ROOT))
    sys.exit(run())
