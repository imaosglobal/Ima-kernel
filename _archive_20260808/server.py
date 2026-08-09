from flask import Flask,request,jsonify
from flask_cors import CORS
import json,os
app=Flask(__name__)
CORS(app)
F="memory.json"

@app.route("/health")
def h():
    return jsonify({"ok":True})

@app.route("/brain",methods=["POST"])
def b():
    d=request.get_json()
    m=d.get("message","")
    mem={"chats":[]}
    if os.path.exists(F):
        mem=json.load(open(F,"r"))
    mem["chats"].append(m)
    json.dump(mem,open(F,"w"),ensure_ascii=False,indent=2)
    return jsonify({"reply":f"שמעתי: {m}"})

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5001)
