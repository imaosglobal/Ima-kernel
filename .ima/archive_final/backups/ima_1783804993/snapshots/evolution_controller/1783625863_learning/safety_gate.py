def check_action(action, reason):

    blocked = [
        "delete",
        "remove",
        "format",
        "password",
        "credential"
    ]

    text = f"{action} {reason}".lower()

    for item in blocked:
        if item in text:
            return {
                "approved": False,
                "reason": f"blocked keyword: {item}"
            }

    return {
        "approved": True,
        "reason": "safe action"
    }
