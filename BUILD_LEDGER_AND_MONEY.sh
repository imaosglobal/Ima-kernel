#!/bin/bash
echo "=== בונה Ledger + פקודות כסף מזוייף ==="

touch .ima/ledger.jsonl

cat > ima_ledger.py << 'EOL'
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
EOL

mkdir -p commands
cat > commands/money_commands.py << 'EOL'
from ima_ledger import add_tx, get_balance
def cmd_deposit(user, amount):
    add_tx(user, "deposit", float(amount), "TESTNET MONEY")
    return f"הופקד {amount} טוקני טסט. יתרה: {get_balance(user)}"
def cmd_balance(user):
    return f"יתרתך: {get_balance(user)} טוקני טסט"
EOL

git add .
git commit -m "Add: ledger.jsonl + money commands for simulation"
echo "=== DONE. ledger ופקודות כסף מוכנים ==="
