from ima_ledger import add_tx, get_balance
def cmd_deposit(user, amount):
    add_tx(user, "deposit", float(amount), "TESTNET MONEY")
    return f"הופקד {amount} טוקני טסט. יתרה: {get_balance(user)}"
def cmd_balance(user):
    return f"יתרתך: {get_balance(user)} טוקני טסט"
