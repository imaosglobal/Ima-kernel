from __future__ import annotations

import time


def execute_outreach(context):
    """
    Controlled outbound gateway.

    Default mode is dry_run=True.
    No external message is sent unless an explicit
    live connector is supplied by the caller.
    """

    target = str(context.get("target", "organization"))
    message = str(
        context.get(
            "message",
            f"שלום, IMA מזהה אפשרות לשיתוף פעולה עם {target}",
        )
    )

    dry_run = bool(context.get("dry_run", True))

    result = {
        "action": "create_personal_outreach",
        "target": target,
        "message": message,
        "mode": "dry_run" if dry_run else "live",
        "timestamp": time.time(),
    }

    if dry_run:
        result["status"] = "prepared"
        result["external_action"] = False
        return result

    connector = context.get("connector")

    if connector is None:
        result["status"] = "blocked"
        result["external_action"] = False
        result["error"] = "No outbound connector configured"
        return result

    try:
        external_result = connector(
            target=target,
            message=message,
        )

        result["status"] = "sent"
        result["external_action"] = True
        result["external_result"] = external_result

    except Exception as exc:
        result["status"] = "failed"
        result["external_action"] = False
        result["error"] = str(exc)

    return result
