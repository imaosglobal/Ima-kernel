"""
IMA ONE BRAIN
Canonical runtime entrypoint / compatibility bridge.

This file is the runtime entrypoint expected by the Termux
ima_learning service.

It delegates actual intelligence work to the existing canonical
IMA engines instead of duplicating their logic.
"""

from datetime import datetime
import json
import traceback
from pathlib import Path


ROOT = Path(__file__).resolve().parent
STATUS_FILE = ROOT / "startup" / "ima_memory.json"


def _run_master_cycle():
    """
    Primary learning/intelligence path.
    """
    from founder.executive_ai.unified_brain.master_cycle import run
    return run()


def _run_autonomous_cycle():
    """
    Secondary autonomous action path.

    The action engine is optional: learning must remain available
    even if the action layer is unavailable.
    """
    try:
        from founder.executive_ai.action_engine.autonomous_cycle import run_cycle
        return run_cycle()
    except Exception as exc:
        return {
            "status": "action_engine_unavailable",
            "error": repr(exc),
        }


def _status_payload(brain=None, autonomous=None):
    return {
        "time": datetime.now().isoformat(),
        "system": "IMA ONE BRAIN",
        "components": [
            {
                "component": "unified_brain",
                "status": "ok" if brain is not None else "error",
                "result": brain,
            },
            {
                "component": "master_learning",
                "status": "ok" if brain is not None else "error",
                "result": (
                    brain.get("learning")
                    if isinstance(brain, dict)
                    else brain
                ),
            },
            {
                "component": "autonomous_cycle",
                "status": (
                    "ok"
                    if isinstance(autonomous, dict)
                    and autonomous.get("status") != "action_engine_unavailable"
                    else "degraded"
                ),
                "result": autonomous,
            },
        ],
        "status": "running",
    }


def write_status(payload):
    """
    Preserve the historical status location used by IMA.
    """
    try:
        STATUS_FILE.parent.mkdir(parents=True, exist_ok=True)

        # Read existing ima_memory.json when possible.
        existing = {}
        if STATUS_FILE.exists():
            try:
                existing = json.loads(
                    STATUS_FILE.read_text(
                        encoding="utf-8",
                        errors="ignore"
                    )
                )
            except Exception:
                existing = {}

        existing["ima_one_brain_status.json"] = json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
        )

        STATUS_FILE.write_text(
            json.dumps(
                existing,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    except Exception as exc:


def run():
    """
    Execute one complete IMA ONE BRAIN cycle.
    """

    brain = None
    autonomous = None

    try:
        brain = _run_master_cycle()
    except Exception as exc:
        traceback.print_exc()

    try:
        autonomous = _run_autonomous_cycle()
            json.dumps(
                autonomous,
                ensure_ascii=False,
                indent=2,
                default=str,
            )
        )
    except Exception as exc:
        autonomous = {
            "status": "error",
            "error": repr(exc),
        }

    payload = _status_payload(
        brain=brain,
        autonomous=autonomous,
    )

    write_status(payload)


    return payload


def main():
    return run()


if __name__ == "__main__":
    main()
