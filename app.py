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
