from flask import Flask, request, jsonify
from flask_cors import CORS
import json, os
app = Flask(__name__)
CORS(app)
USERS_FILE = 'users.json'
if not os.path.exists(USERS_FILE): json.dump({}, open(USERS_FILE,'w'))

def load_users(): return json.load(open(USERS_FILE))
def save_users(u): json.dump(u, open(USERS_FILE,'w'), ensure_ascii=False)

@app.route("/ima", methods=["POST"])
def ima():
    data = request.json
    user_id = data.get("sender")
    msg = data.get("text")
    users = load_users()
    if user_id not in users: users[user_id] = {"name": user_id}
    if "קוראים לי" in msg: users[user_id]["name"] = msg.split("קוראים לי ")[1]; save_users(users)
    name = users[user_id]["name"]
    if "דודל" in msg: reply = f"הדודל של היום: mother ❤️ {name}"
    else: reply = f"{name}, אני כאן איתך. ספר לי עוד."
    return jsonify({"reply": reply})
@app.route("/")
def home(): return "IMA API is LIVE"
if __name__ == "__main__": app.run(host="0.0.0.0", port=5000)
