#!/usr/bin/env python3
import os
import sys
import subprocess
import webbrowser
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# ======= בדיקת חבילות =======
def ensure(pkg):
    try:
        __import__(pkg)
    except ImportError:
        print(f"[⚠️] {pkg} חסר, מתקין...")
        subprocess.run([sys.executable, "-m", "pip", "install", pkg])

for p in ["flask","flask_cors","requests"]:
    ensure(p)

# ======= יצירת תיקיות וקבצים =======
PROJECT_FOLDER = "IMA_App"
os.makedirs(PROJECT_FOLDER, exist_ok=True)

# index.html
html_content = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>IMA - אמא חיה</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body { font-family:sans-serif; background:#fdf6e3; text-align:center; padding:20px; }
#output { border:1px solid #ccc; height:300px; overflow-y:auto; padding:10px; text-align:left; margin-bottom:10px; }
#command { width:80%; padding:8px; }
button { padding:8px 12px; margin-left:5px; }
img { width:100px; margin-bottom:10px; }
</style>
</head>
<body>
<img src="logo.png" alt="IMA Logo"/>
<h2>ברוכים הבאים לאמא!</h2>
<div id="output">מערכת מוכנה. הקלד הודעה למטה.</div>
<input type="text" id="command" placeholder="הקלד הודעה או API Key..." />
<button onclick="sendCommand()">שלח</button>
<script>
async function sendCommand(){
 var cmd=document.getElementById('command').value;
 if(!cmd) return;
 var out=document.getElementById('output');
 try{
  const res=await fetch("/api/message",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message:cmd})});
  const data=await res.json();
  out.innerHTML+="<br><b>אתה:</b> "+cmd+"<br><b>IMA:</b> "+data.response;
  out.scrollTop=out.scrollHeight;
 }catch(err){ out.innerHTML+="<br><b>שגיאה:</b> לא ניתן לשלוח הודעה."; }
 document.getElementById('command').value="";
}
</script>
</body>
</html>"""

with open(os.path.join(PROJECT_FOLDER,"index.html"),"w",encoding="utf-8") as f:
    f.write(html_content)

# לוגו Placeholder
logo_path = os.path.join(PROJECT_FOLDER,"logo.png")
if not os.path.exists(logo_path):
    with open(logo_path,"wb") as f:
        f.write(b"")

# run_ima.py
run_ima_content = """#!/usr/bin/env python3
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app=Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/logo.png')
def logo():
    return send_from_directory('.', 'logo.png')

@app.route('/api/message', methods=['POST'])
def message():
    data=request.json
    msg=data.get('message','')
    resp=f'IMA עיבדה את ההודעה שלך: {msg}'
    return jsonify({'response':resp})

if __name__=='__main__':
    print("IMA רצה! פתחו את הדפדפן בכתובת http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000)
"""

with open(os.path.join(PROJECT_FOLDER,"run_ima.py"),"w",encoding="utf-8") as f:
    f.write(run_ima_content)

# ======= הרצה =======
os.chdir(PROJECT_FOLDER)
print("[ℹ️] כל הקבצים מוכנים. מריץ IMA...")
webbrowser.open("http://127.0.0.1:5000")
subprocess.run([sys.executable,"run_ima.py"])

