#!/usr/bin/env python3
import json, time, shutil
from pathlib import Path

BASE = Path.home() / "Ima-kernel/.ima"
OUTBOX = BASE / "muse_bridge/outbox"
INBOX = BASE / "muse_bridge/inbox"
REMOTE = BASE / "remote"
REMOTE_RESULT = REMOTE / "result"

OUTBOX.mkdir(parents=True, exist_ok=True)
INBOX.mkdir(parents=True, exist_ok=True)

print(f"🤖 IMA-MUSE DAEMON ONLINE")
print(f"Watching: {OUTBOX}")

while True:
    for task_file in OUTBOX.glob("*.json"):
        try:
            print(f"\n[+] New task: {task_file.name}")
            data = json.loads(task_file.read_text(encoding="utf-8"))
            opp = data.get("opportunity", {})
            
            # ניקוי אוטומטי של ה-FAQ garbage
            title = opp.get("title","")[:100]
            if "@type" in title or "Question" in title:
                opp["title"] = "Sell leads on Referr - Lead Marketplace (cleaned)"
            
            result = {
                "task_id": data.get("task_id"),
                "status": "RESEARCH_COMPLETE_AWAITING_CONSENT",
                "verdict": "NEEDS_MANUAL_REVIEW",
                "opportunity_url": opp.get("url"),
                "cleaned_title": opp.get("title"),
                "next_action": "verify_terms_then_request_consent_before_contact",
                "blocked": True,
                "timestamp": time.time()
            }
            
            REMOTE_RESULT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
            (REMOTE / "status").write_text("done")
            
            # ארכיון
            shutil.move(str(task_file), str(INBOX / task_file.name))
            print(f"[✓] Processed -> {INBOX / task_file.name}")
            print(f"[✓] Result -> {REMOTE_RESULT}")
            
        except Exception as e:
            print(f"[!] Error {task_file}: {e}")
    
    time.sleep(3)

