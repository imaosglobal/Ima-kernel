def rank_leads(context):

    leads=context.get("leads",[])

    ranked=[]

    for lead in leads:
        ranked.append({
            "name":lead.get("name"),
            "type":lead.get("type"),
            "score":80,
            "reason":"Potential IMA fit"
        })

    return {
        "action":"rank_leads",
        "ranked":ranked
    }
