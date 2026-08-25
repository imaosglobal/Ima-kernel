#!/bin/bash
echo "=== מתקן ייבוא + מוסיף ראוטים ==="

# 1. מעביר את הפונקציות ל-ima_ledger.py כדי ש-app.py ימצא אותן
cat > ima_ledger.py << 'EOL'
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
EOL

# 2. מעדכן את app.py שיעבוד
cat > app.py << 'EOL'
from flask import Flask, render_template_string, request
from ima_ledger import cmd_deposit, cmd_balance

app = Flask(__name__)
USER = "test_user"

HTML = """
<h1>IMA Bank - TESTNET</h1>
<p><b>יתרה:</b> {{balance}}</p>
<form method=post>
  <input name=amount placeholder="סכום להפקדה" type=number step=0.01>
  <button name=action value=deposit>הפקד</button>
</form>
<p style=color:green>{{msg}}</p>
"""

@app.route("/", methods=["GET","POST"])
def home():
    msg = ""
    if request.method == "POST":
        amount = request.form["amount"]
        if amount:
            msg = cmd_deposit(USER, amount)
    bal = cmd_balance(USER)
    return render_template_string(HTML, balance=bal, msg=msg)

if __name__ == "__main__":
    print("IMA Bank running on http://localhost:8080")
    app.run(host="0.0.0.0", port=8080, debug=True)
EOL

git add.
git commit -m "IMA v2.3.1: Fix import - move commands to ima_ledger.py"
git push origin master

echo "=== תיקון הושלם. מריץ שוב ==="
python app.py
