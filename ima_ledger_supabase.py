import os
# TODO: להחליף ל supabase-py
def add_tx(user, type, amount, note=""):
    print(f"[SUPABASE DEV] {user} {type} {amount}")
    return {"status": "ok"}
def get_balance(user):
    return 1000.0 # MOCK עד החיבור
