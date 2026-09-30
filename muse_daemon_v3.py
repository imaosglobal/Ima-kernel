#!/usr/bin/env python3
import json, time, shutil, re
from pathlib import Path
import urllib.request

BASE = Path.home() / "Ima-kernel/.ima"
OUTBOX = BASE / "muse_bridge/outbox"
INBOX = BASE / "muse_bridge/inbox"
PROCESSED = BASE / "muse_bridge/processed"
REMOTE = BASE / "remote"
LOG = REMOTE / "daemon.log"
RESULT = REMOTE / "result"

def clean(text):
    if not text: return ""
    # V3 - מסיר הכל עד למשפט האמיתי
    if "Simply browse" in text:
        text = text.split("Simply browse")[-1]
        text = "Simply browse " + text
    text = re.sub(r'^.*?to the referral.*?},','', text)
    text = re.sub(r'^\W+', '', text)
    text = text[:400].strip()
    return text

def log(m):
    print(m)
    open(LOG,"a",encoding="utf-8").write(f"[{time.strftime('%H:%M:%S')}] {m}\n")

log("🚀 V3 CLEANER ONLINE")

while True:
    for f in OUTBOX.glob("*.json"):
        try:
            data = json.loads(f.read_text())
            opp = data.get("opportunity",{})
            raw_sig = opp.get("signal","")
            title = opp.get("title","")
            
            # ניקוי אגרסיבי
            if "@type" in title:
                title = "Referr - Lead Marketplace"
            signal = clean(raw_sig)
            if not signal or len(signal)<20:
                signal = "Sell leads: browse requests, submit lead, get paid via Stripe (3% fee min £3)"

            res = {
                "protocol":"IMA-MUSE-TASK/3",
                "task_id": data.get("task_id"),
                "verdict":"VALID_NEEDS_USER_APPROVAL",
                "cleaned_opportunity":{
                    "title": title,
                    "signal": signal,
                    "url": opp.get("url"),
                    "category": opp.get("category")
                },
                "safety":{"consent_required":True, "blocked":["send_message","purchase"]},
                "timestamp": time.time()
            }
            RESULT.write_text(json.dumps(res, indent=2, ensure_ascii=False))
            (REMOTE/"status").write_text("done")
            shutil.move(str(f), str(INBOX/f.name))
            (PROCESSED/f.name).write_text(json.dumps(res, indent=2, ensure_ascii=False))
            log(f"✓ {f.name} -> {title} | {signal[:60]}")
        except Exception as e:
            log(f"! {e}")
    time.sleep(2)
