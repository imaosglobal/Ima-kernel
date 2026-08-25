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
