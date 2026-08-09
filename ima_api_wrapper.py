from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)

@app.route("/ima", methods=["POST"])
def ima():
    data = request.json
    text = data.get("text", "")
    # מריץ את ima.py האמיתי
    result = subprocess.run(
        ["python", ".ima/CANONICAL_AUTHORITY/ACTIVE/ima.py", "ask", text],
        capture_output=True, text=True
    )
    return jsonify({"reply": result.stdout})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
