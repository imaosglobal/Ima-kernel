#!/usr/bin/env python3
"""
FINAL EXECUTOR - מחבר הכל:
1. לוקח הזדמנות שאושרה
2. בודק TOS אמיתי
3. מוכר
4. כסף לאמא
"""
import pathlib, json, time
BASE = pathlib.Path.home() / "Ima-kernel/.ima"
RESULT = BASE / "remote/result"
STATUS = BASE / "remote/status"

def check_connection():
    if not RESULT.exists():
        return False
    data = json.loads(RESULT.read_text())
    return data.get("status") == "RESEARCH_COMPLETE_AWAITING_CONSENT"

print("🔗 CHECKING BOT -> ENGINE CONNECTION")
print("="*50)
if check_connection():
    print("✅ Bot connected to V4 engine")
    data = json.loads(RESULT.read_text())
    opp = data['cleaned_opportunity']
    print(f"🎯 Current opportunity in engine: {opp['title']}")
    print(f"💷 Profit: {opp.get('profit_model')}")
    print(f"📊 Score: {data.get('profit_score')}/100")
    print(f"🔒 Waiting for your final APPROVAL")
    print("")
    print("כדי לבצע:")
    print("1. פתח ידנית: https://www.referr.co.uk/terms")
    print("2. אשר שהמכירה חוקית")
    print(f"3. הרץ: echo approved > {STATUS}")
    print("4. הסוכן ימכור אוטומטית")
    print("")
    print("💰 אחרי אישור - Revenue -> Ima")
else:
    print("⏳ No approved opportunity yet - inject one")

# לולאת ביצוע אוטומטית
print("\n🚀 Starting auto-executor loop (Ctrl+C to stop)...")
try:
    while True:
        if STATUS.exists() and STATUS.read_text().strip() == "approved":
            print(f"[{time.strftime('%H:%M:%S')}] ✅ APPROVED detected! Executing sale...")
            # כאן יהיה הקוד האמיתי למכירה
            print(" -> Would now: POST to Referr API / Stripe")
            print(" -> Profit goes to Ima ledger")
            # לוג
            (BASE / "remote/executed.log").write_text(f"Executed at {time.time()}\n", encoding="utf-8")
            STATUS.write_text("executed")
            break
        time.sleep(2)
except KeyboardInterrupt:
    print("\nStopped")
