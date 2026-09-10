def rank_leads(context):

    if context is None:
        context = {}

    leads = context.get("leads", [])

    ranked = []

    for lead in leads:

        ranked.append({
            "name": lead.get("name"),
            "type": lead.get("type"),
            "score": 80,
            "reason": "Potential IMA fit",
        })

    ranked.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return {
        "action": "rank_leads",
        "ranked": ranked,
    }
