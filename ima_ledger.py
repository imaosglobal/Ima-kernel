import json, time, os
LEDGER_PATH = ".ima/ledger.jsonl"
BALANCE_CACHE = {}

def add_tx(user, type, amount, note=""):
    tx = {"ts": time.time(), "user": user, "type": type, "amount": amount, "note": note}
    with open(LEDGER_PATH, "a") as f: f.write(json.dumps(tx) + "\n")
    BALANCE_CACHE[user] = None # מאפס מטמון
    return tx

def get_balance(user):
    if user in BALANCE_CACHE and BALANCE_CACHE[user] is not None:
        return BALANCE_CACHE[user]
    bal = 0
    if not os.path.exists(LEDGER_PATH): return 0
    with open(LEDGER_PATH, "r") as f:
        for line in f:
            if line.strip():
                tx = json.loads(line)
                if tx["user"] == user:
                    bal += tx["amount"] if tx["type"] == "deposit" else -tx["amount"]
    BALANCE_CACHE[user] = bal
    return bal

def cmd_deposit(user, amount):
    add_tx(user, "deposit", float(amount), "TESTNET MONEY")
    return f"הופקד {amount} טוקני טסט. יתרה: {get_balance(user)}"

def cmd_balance(user):
    return f"יתרתך: {get_balance(user)} טוקני טסט"
