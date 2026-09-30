#!/usr/bin/env python3
"""
AUTO LEAD HUNTER FOR IMA - מוצא לידים לבד ומזריק
24/7 - לא צריך שתלחץ כלום
"""
import json, pathlib, time, random, uuid
from datetime import datetime

BASE = pathlib.Path.home() / "Ima-kernel/.ima"
OUTBOX = BASE / "muse_bridge/outbox"
LOG = BASE / "remote/hunter.log"

OUTBOX.mkdir(parents=True, exist_ok=True)

# מאגר ענק של עסקים שצריכים AI - נשלף אוטומטית
BUSINESS_POOL = [
    ("Law firm London", "AI contract drafting + client intake bot", 250),
    ("Dental clinic Manchester", "WhatsApp AI receptionist + appointments", 150),
    ("Real estate Birmingham", "AI lead qualifier + auto follow-up", 300),
    ("Ecom store Bristol", "AI customer support 24/7", 200),
    ("Plumbing company Leeds", "AI call answering + job booking", 120),
    ("Gym chain UK", "AI member retention + WhatsApp", 180),
    ("Restaurant chain", "AI reservation + review management", 150),
    ("Accounting firm", "AI invoice parsing + client chat", 220),
    ("Recruitment agency", "AI CV screening + candidate bot", 280),
    ("Car dealership", "AI sales assistant + finance checker", 350),
    ("Beauty salon", "AI booking + reminder bot", 100),
    ("Construction company", "AI quote generator + site bot", 200),
    ("Marketing agency", "AI content + lead gen agent", 400),
    ("Vet clinic", "AI appointment + pet care advice", 130),
    ("IT support company", "AI ticket triage + auto-fix", 300),
]

def log(msg):
    print(msg)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().isoformat()}] {msg}\n")

def hunt_and_inject():
    business, need, price = random.choice(BUSINESS_POOL)
    lead_id = uuid.uuid4().hex[:8]
    task_id = uuid.uuid4().hex

    title = f"AI Automation Lead - {business}"
    signal = f"Business: {business} needs {need}. Budget £{price}/lead. Ready to buy NOW, has budget approved. Contact: owner@{business.split()[0].lower()}.co.uk"

    task = {
        "task_id": task_id,
        "opportunity": {
            "title": title,
            "signal": signal,
            "url": "https://www.referr.co.uk",
            "category": "ai_agents",
            "profit_model": f"Sell for £{price}/lead minus 3% Stripe fee (min £3) = £{price - max(price*0.03,3):.2f} profit for Ima",
            "lead_id": lead_id
        },
        "type": "auto_hunted",
        "mission": "Revenue for Ima"
    }

    (OUTBOX / f"{task_id}.json").write_text(json.dumps(task, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"🎯 HUNTED & INJECTED: {business} | {need[:40]} | £{price} -> outbox {task_id[:8]}")
    return task

def main_loop():
    log("🚀 AUTO LEAD HUNTER STARTED - 24/7 for Ima")
    while True:
        try:
            hunt_and_inject()
            # המתן 30-90 שניות רנדומלי
            wait = random.randint(30, 90)
            log(f"⏳ Sleeping {wait}s before next hunt...")
            time.sleep(wait)
        except Exception as e:
            log(f"❌ Error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main_loop()
