"""
Impact Engine - בוחר איפה להשקיע את 10% של הקרן
חינוך, בריאות, אקלים
"""
def allocate_impact_funds(amount):
    """מחלק את כספי האימפקט"""
    if amount <= 0:
        return {"status": "no_funds"}
    
    # 40% חינוך, 30% בריאות, 30% אקלים
    allocation = {
        "education": amount * 0.4,
        "health": amount * 0.3,
        "climate": amount * 0.3
    }
    
    return {
        "status": "allocated",
        "total": amount,
        "allocation": allocation,
        "note": "DRY-RUN: No real transfer yet"
    }
