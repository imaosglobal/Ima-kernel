from flask import Flask, request, jsonify
from pathlib import Path
import sys, os, json, traceback

env_path = Path(".env")
if env_path.exists():
    for line in env_path.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k,v = line.split("=",1)
            os.environ[k] = v.strip('"')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ima_system import answer

app = Flask(__name__)

def load_memory():
    default = {"users": {}, "conversations": [], "facts": {}, "last_language": "he"}
    p = Path(".ima/memory.json")
    p.parent.mkdir(exist_ok=True)
    try:
        if p.exists():
            data = json.loads(p.read_text())
            if not isinstance(data, dict):
                data = default # אם זה רשימה - מאפס
        else: data = default
    except: data = default
    p.write_text(json.dumps(data))
    return data

@app.route("/")
def home():
    return "IMA API is LIVE. Send POST to /chat"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        load_memory() # מוודא שה-memory תקין
        data = request.get_json()
        q = data.get("question", "")
        res = answer(q, [])
        return jsonify({"text": res['text'], "confidence": res['confidence']})
    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
