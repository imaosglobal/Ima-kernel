#!/bin/bash
echo "=== בונה UI ווב ל-IMA עם חיבור לסופבייס ==="

# 1. UI פשוט עם כפתורי הפקדה ויתרה
cat > app.py << 'EOL'
from flask import Flask, render_template_string, request
from ima_ledger import cmd_deposit, cmd_balance

app = Flask(__name__)
USER = "test_user"

HTML = """
<h1>IMA Bank - TESTNET</h1>
<p><b>יתרה:</b> {{balance}}</p>
<form method=post>
  <input name=amount placeholder="סכום להפקדה">
  <button name=action value=deposit>הפקד</button>
</form>
"""

@app.route("/", methods=["GET","POST"])
def home():
    if request.method == "POST":
        amount = request.form["amount"]
        result = cmd_deposit(USER, amount)
        return result + "<br><a href='/'>חזור</a>"
    bal = cmd_balance(USER)
    return render_template_string(HTML, balance=bal)

if __name__ == "__main__": app.run(host="0.0.0.0", port=8080)
EOL

# 2. מתקין פלאסק
pip install flask

# 3. מעדכן ledger לעבוד עם סופבייס DEV
cat > ima_ledger_supabase.py << 'EOL'
import os
# TODO: להחליף ל supabase-py
def add_tx(user, type, amount, note=""):
    print(f"[SUPABASE DEV] {user} {type} {amount}")
    return {"status": "ok"}
def get_balance(user):
    return 1000.0 # MOCK עד החיבור
EOL

git add .
git commit -m "IMA v2.3: Add Web UI + Supabase connector for TESTNET"
git push origin master

echo "=== מוכן. מריץ את השרת ==="
echo "הרץ: python app.py"
echo "ואז כנס ל: http://localhost:8080"
