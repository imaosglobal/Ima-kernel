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
from ima_system import answer, load_memory

app = Flask(__name__)

# FORCE RESET CORRUPTED MEMORY ON BOOT
def force_fix_memory():
    p = Path(".ima/memory_v2.json")
    p.parent.mkdir(exist_ok=True)
    try:
        data = json.loads(p.read_text())
        if not isinstance(data, dict):
            raise ValueError("memory is list")
    except:
        data = {"users": {}, "conversations": [], "facts": {}, "last_language": "he"}
        p.write_text(json.dumps(data))

force_fix_memory()

@app.route("/")
def home():
    return "IMA API is LIVE. Send POST to /chat"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        force_fix_memory() # מאפס לפני כל בקשה
        data = request.get_json()
        q = data.get("question", "")
        res = answer(q, [])
        return jsonify({"text": res['text'], "confidence": res['confidence']})
    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
