# PATCH - מוסיף דיספאצ'ר חדש ל-orchestrator הקיים
from founder.executive_ai.treasury.treasury_engine import deposit_revenue
from founder.executive_ai.treasury.impact_engine import allocate_impact_funds
from founder.executive_ai.education.education_engine import create_personal_learning_plan

def dispatch_new_actions(action_name, action):
    """מתחבר ל-dispatcher הקיים בשורה 88"""
    
    if action_name == "execute_revenue":
        # כשיש actual_outcome עם כסף
        amount = action.get("actual_outcome", {}).get("revenue", 0)
        return deposit_revenue(amount, action)
    
    if action_name == "allocate_impact":
        amount = action.get("amount", 0)
        return allocate_impact_funds(amount)
        
    if action_name == "create_education_plan":
        child_id = action.get("target")
        return create_personal_learning_plan(child_id, action.get("needs", {}))
    
    return None
