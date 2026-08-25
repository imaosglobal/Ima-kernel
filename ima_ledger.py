BALANCE_CACHE = {}
import json, time, os
LEDGER_PATH = ".ima/ledger.jsonl"
def add_tx(user, type, amount, note=""):
    tx = {"ts": time.time(), "user": user, "type": type, "amount": amount, "note": note}
    with open(LEDGER_PATH, "a") as f: f.write(json.dumps(tx) + "\n")
    return tx
def get_balance(user):
    bal = 0
    if not os.path.exists(LEDGER_PATH): return 0
    with open(LEDGER_PATH, "r") as f:
        for line in f:
            tx = json.loads(line)
            if tx["user"] == user:
                bal += tx["amount"] if tx["type"] == "deposit" else -tx["amount"]
    return bal
