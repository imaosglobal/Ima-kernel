#!/usr/bin/env python3
import json, pathlib
BASE = pathlib.Path.home() / "Ima-kernel/.ima"
RESULT = BASE / "remote/result"
ALL = BASE / "all_opportunities.jsonl"

def show():
    if not RESULT.exists():
        print("⏳ ממתין להזדמנות...")
        return
    data = json.loads(RESULT.read_text(encoding="utf-8"))
    opp = data.get("cleaned_opportunity",{})
    print(f"""
💎 IMA RICH ENGINE V4

🎯 {opp.get('title')}
📂 קטגוריה: {opp.get('category')}
💰 מודל: {opp.get('profit_model')}
📈 ציון לאמא: {data.get('profit_score', 0)}/100
🔗 {opp.get('url')}
📝 {opp.get('signal','')[:350]}

🤖 Muse + GPT + עתידיים | 🔒 צריך אישור שלך
Mission: {data.get('mission','')}

""")
    if ALL.exists():
        print(f"📊 סהכ נסרקו: {len(ALL.read_text().strip().splitlines())} הזדמנויות")

if __name__ == "__main__":
    show()
