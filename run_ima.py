#!/usr/bin/env python3
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)

# ===== Frontend HTML =====
html_content = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>IMA - אמא חיה</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body { font-family: sans-serif; background:#fdf6e3; padding:20px; text-align:center; }
#output { border:1px solid #ccc; padding:10px; height:300px; overflow-y:auto; margin-bottom:10px; text-align:left; }
#command { width:80%; padding:8px; }
button { padding:8px 12px; margin-left:5px; }
img { width:100px; margin-bottom:10px; }
</style>
</head>
<body>
<img src="logo.png" alt="IMA Logo"/>
<h2>ברוכים הבאים לאמא!</h2>
<div id="output">המערכת מוכנה. הקלד פקודה למטה.</div>
<input type="text" id="command" placeholder="הקלד פקודה..." />
<button onclick="sendCommand()">שלח</button>

<script>
// כל הלוגיקה עוברת כאן בדפדפן
function sendCommand() {
    var cmd = document.getElementById('command').value;
    if (!cmd) return;

    // לדוגמה: כל הפקודות יעובדו כאן
    var output = document.getElementById('output');
    var response = "IMA עיבדה את הפקודה שלך ב-JS: " + cmd;
    
    output.innerHTML += "<br><b>אתה:</b> "+cmd;
    output.innerHTML += "<br><b>IMA:</b> "+response;
    output.scrollTop = output.scrollHeight;
    document.getElementById('command').value="";
}
</script>
</body>
</html>
"""

with open("index.html","w", encoding="utf-8") as f:
    f.write(html_content)

# ===== Flask routes =====
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# פתיחת Chrome
url = 'http://127.0.0.1:5000'
print("IMA רצה! פתחו את הדפדפן בכתובת:", url)
try:
    subprocess.Popen(['am', 'start', '-a', 'android.intent.action.VIEW', '-d', url])
except:
    print("לא הצלחנו לפתוח אוטומטית. פתחו את Chrome וגלשו לכתובת.")

# הפעלת Flask server
app.run(host='0.0.0.0', port=5000)
