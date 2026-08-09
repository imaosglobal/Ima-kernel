#!/data/data/com.termux/files/usr/bin/bash
echo "IMA OS - מצב עדכון בטוח. לא מוחק כלום"

# 1. BACKEND - יוצר רק אם לא קיים
if [! -f backend/app.py ]; then
cat > backend/app.py << 'EOF'
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
EOF
echo "נוצר backend/app.py חדש"
else
echo "backend/app.py כבר קיים. לא נוגע"
fi

# 2. FRONTEND - יוצר רק אם לא קיים
if [! -f frontend/index.html ]; then
cat > frontend/index.html << 'EOF'
<!DOCTYPE html><html lang="he" dir="rtl"><head><meta charset="UTF-8"><title>IMA - העוזרת שלך בוואצאפ</title>
<script src="https://cdn.tailwindcss.com"></script><link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;900&display=swap" rel="stylesheet">
</head><body class="bg-gradient-to-b from-purple-50 to-white text-gray-900" style="font-family:Heebo">
<header class="bg-white shadow-sm"><div class="max-w-6xl mx-auto flex items-center justify-between p-4">
<img src="https://i.imgur.com/JzWqZkB.png" class="w-12 h-12 rounded-full"><span class="font-black text-2xl text-purple-600">IMA</span>
<button class="bg-purple-600 text-white px-5 py-2 rounded-lg font-bold">התחבר עם גוגל</button></div></header>
<section class="text-center py-20 px-4"><h1 class="text-5xl font-black mb-4">העוזרת האישית שלך, בוואצאפ</h1>
<p class="text-xl text-gray-600 mb-8">IMA זוכרת, לומדת, ומתאימה את עצמה רק אליך. עם דודל, GLB, וקול.</p>
<a href="https://wa.me/972XXXXXXXXX" class="bg-green-500 text-white px-8 py-4 rounded-full font-black text-lg">דבר עם IMA בוואצאפ</a>
<div class="bg-white p-6 rounded-2xl shadow-xl max-w-2xl mx-auto mt-12">
<div id="chat-demo" class="h-64 overflow-y-auto text-right space-y-3 mb-4"></div>
<div class="flex gap-2"><input id="msg" class="flex-1 border rounded-lg px-4 py-2"><button onclick="send()" class="bg-purple-600 text-white px-6 py-2 rounded-lg">שלח</button></div>
</div></section>
<script>
async function send(){
let t=document.getElementById("msg").value; if(!t) return;
let chat=document.getElementById("chat-demo");
chat.innerHTML+=`<div class="bg-purple-600 text-white p-3 rounded-2xl inline-block">${t}</div><br>`;
let r=await fetch("http://10.100.102.6:5000/ima",{method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({text:t, sender:"guest"})});
let d=await r.json();
chat.innerHTML+=`<div class="bg-gray-200 p-3 rounded-2xl inline-block">${d.reply}</div><br>`;
document.getElementById("msg").value=""; chat.scrollTop=99999;
}</script></body></html>
EOF
echo "נוצר frontend/index.html חדש"
else
echo "frontend/index.html כבר קיים. לא נוגע"
fi

echo "סיים בדיקה. מריץ שרתים..."
pkill -f gunicorn; pkill -f serve
cd backend && nohup gunicorn -w 2 -b 0.0.0.0:5000 app:app >../ima.log 2>&1 &
cd../frontend && serve -s. -l 8080 &
echo "האתר: http://10.100.102.6:8080"
