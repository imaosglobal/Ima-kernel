def create_messages(context):

    target=context.get(
        "target",
        "organization"
    )

    return {
        "action":"generate_outreach",
        "target":target,
        "messages":[
            f"שלום, IMA מזהה אפשרות לשיתוף פעולה עם {target}"
        ]
    }
