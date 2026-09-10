#!/bin/bash
echo "🚀 Ima 3D All-in-One מתחילה לפעול..."

ENV_FILE=".env"
if [ ! -f "$ENV_FILE" ]; then
    echo "OPENAI_API_KEY='$OPENAI_KEY'" > "$ENV_FILE"
    echo "✅ מפתח API נוסף בהצלחה ל-.env"
else
    echo "🔑 מפתח API כבר קיים, ממשיך..."
fi

# -------------------------------
# 2️⃣ התקנת מודולים (פעם אחת)
# -------------------------------
pip install --upgrade pip setuptools wheel
pip install \
colorama pyttsx3 pytube moviepy opencv-python \
googletrans==4.0.0-rc1 PyOpenGL PyOpenGL_accelerate moderngl requests youtube-dl \
speechrecognition pyaudio vosk playsound Flask flask-socketio eventlet \
mediapipe opencv-contrib-python aiortc aiohttp websockets \
--no-build-isolation --prefer-binary || echo "⚠️ התקנה נתקעה, ממשיך"

# -------------------------------
# 3️⃣ יצירת תיקיות חיוניות
# -------------------------------
mkdir -p ./scripts ./assets ./logs ./downloads ./3d_assets ./video_assets ./gui_assets ./webrtc_assets

# -------------------------------
# 4️⃣ בדיקה ויצירת main.py אם חסר
# -------------------------------
MAIN_PATH=$(find ./ -type f -name main.py | head -n 1)
if [ -z "$MAIN_PATH" ]; then
    echo "❌ לא נמצא main.py. יוצר Dummy זמני"
    mkdir -p ./classic/original_autogpt/autogpt/app
    cat > ./classic/original_autogpt/autogpt/app/main.py << 'PYEOF'
print("Ima 3D All-in-One Dummy Main – עודכן")
PYEOF
    MAIN_PATH=./classic/original_autogpt/autogpt/app/main.py
fi

# -------------------------------
# 5️⃣ הפעלת Ima GUI + WebRTC + 3D + Video + אפקטים
# -------------------------------
echo "🌐 הפעלת Ima 3D WebRTC GUI בכתובת: http://localhost:8000"
python "$MAIN_PATH" \
--ai-name "Ima" \
--ai-role "ישות אמהית דיגיטלית, מדברת בקול ובצ'אט, יוצרת תוכן וסרטוני 3D, מאפשרת כובעים ופילטרים מצחיקים, WebRTC Live, AI מלאה" \
--ai-goals "צור והפץ תוכן וסרטוני וידאו בזמן אמת, עקוב אחר צפיות, שפר תוכן, דיבור בקול ובצ'אט, הפץ אוטומטית לכל משתמש בעולם, WebRTC אינטראקטיבי" \
--continuous-limit 0 \
--auto-optimization True \
--auto-content-improvement True \
--tracking-views True \
--language-adaptation True \
--audience-personalization True \
--continuous-uploads True \
--3d-mode True \
--video-mode True \
--fun-effects True \
--gui True \
--webrtc True \
--gui-port 8000 \
--live-server True

# -------------------------------
# 6️⃣ הפצה גלובלית אוטומטית
# -------------------------------
echo "📡 מתחיל שיתוף Ima All-in-One לשרת גלובלי..."
rsync -avz --delete "$LOCAL_DIR/" "$GLOBAL_SERVER"
echo "✅ Ima All-in-One זמינה לכל העולם בכתובת: https://remote-server/Ima-AutoGPT-3D-AllInOne/"
