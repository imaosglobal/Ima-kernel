def create_messages(context):

    if context is None:
        context = {}

    target = context.get(
        "target",
        "organization",
    )

    return {
        "action": "generate_outreach",
        "target": target,
        "messages": [
            f"שלום, IMA מזהה אפשרות לשיתוף פעולה עם {target}"
        ],
    }
