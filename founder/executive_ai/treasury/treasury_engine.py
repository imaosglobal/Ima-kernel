"""
Treasury Engine - קרן האם
כל הרווחים נכנסים לכאן. חלוקה: 70% רווח למשתמשים, 20% צמיחה, 10% אימפקט
"""
import time

VAULT = {
    "total_revenue": 0.0,
    "distribution": {"users": 0.7, "growth": 0.2, "impact": 0.1},
    "impact_pool": 0.0
}

def deposit_revenue(amount, source_action):
    """מפקיד רווח לקרן ומחלק אוטומטית"""
    if amount <= 0: 
        return {"status": "no_revenue"}
    
    VAULT["total_revenue"] += amount
    
    users_share = amount * VAULT["distribution"]["users"]
    growth_share = amount * VAULT["distribution"]["growth"] 
    impact_share = amount * VAULT["distribution"]["impact"]
    VAULT["impact_pool"] += impact_share
    
    return {
        "status": "deposited",
        "amount": amount,
        "source": source_action,
        "split": {"users": users_share, "growth": growth_share, "impact": impact_share},
        "vault_total": VAULT["total_revenue"],
        "impact_pool": VAULT["impact_pool"]
    }

def get_vault_status():
    return VAULT
