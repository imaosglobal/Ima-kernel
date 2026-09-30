#!/usr/bin/env python3
import json, time, shutil, re, hashlib
from pathlib import Path
import urllib.request

BASE = Path.home() / "Ima-kernel/.ima"
OUTBOX = BASE / "muse_bridge/outbox"
INBOX = BASE / "muse_bridge/inbox"
PROCESSED = BASE / "muse_bridge/processed"
REMOTE = BASE / "remote"
LOG = REMOTE / "daemon.log"
RESULT = REMOTE / "result"

for p in [OUTBOX, INBOX, PROCESSED, REMOTE]:
    p.mkdir(parents=True, exist_ok=True)

def clean_garbage(text: str) -> str:
    if not text: return ""
    # מסיר את כל ה-JSON-LD FAQ schema שהרס לך את ה-opportunities
    text = re.sub(r'\{"@type".*?\}\}', '', text)
    text = re.sub(r'"@type":"Question".*?paid directly', 'Referr Lead Marketplace - Stripe payout 3% fee', text, flags=re.DOTALL)
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:500]

def verify_url(url: str):
    try:
        req = urllib.request.Request(url, headers={'User-Agent':'IMA-Bot/2.0'})
        with urllib.request.urlopen(req, timeout=10) as r:
            html = r.read().decode('utf-8','ignore')[:5000]
            has_tos = "terms" in html.lower() or "privacy" in html.lower()
            has_stripe = "stripe" in html.lower()
            return {"reachable": True, "has_tos": has_tos, "has_stripe": has_stripe, "status": r.status}
    except Exception as e:
        return {"reachable": False, "error": str(e)}

def log(msg):
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line+"\n")

log("🚀 IMA-MUSE V2 ONLINE - Upgraded Bridge")

while True:
    for task_file in OUTBOX.glob("*.json"):
        try:
            log(f"New task: {task_file.name}")
            data = json.loads(task_file.read_text(encoding="utf-8"))
            opp = data.get("opportunity", {})
            url = opp.get("url","")

            cleaned_title = clean_garbage(opp.get("title",""))
            cleaned_signal = clean_garbage(opp.get("signal",""))

            verification = verify_url(url) if url else {"reachable": False}

            result = {
                "protocol": "IMA-MUSE-TASK/2",
                "task_id": data.get("task_id"),
                "status": "RESEARCH_COMPLETE_AWAITING_CONSENT",
                "verdict": "VALID_NEEDS_USER_APPROVAL" if verification.get("reachable") else "UNREACHABLE_NEEDS_REVIEW",
                "cleaned_opportunity": {
                    "title": cleaned_title or "Sell leads on Referr - Lead Marketplace",
                    "signal": cleaned_signal or "Platform allows selling leads via Stripe",
                    "url": url,
                    "category": opp.get("category","software"),
                },
                "verification": verification,
                "safety": {
                    "consent_required": True,
                    "blocked_actions": data.get("requires_user_approval_for", []),
                    "proof_required": True
                },
                "next_action": "Present cleaned opportunity to user, request explicit consent before contact",
                "timestamp": time.time()
            }

            RESULT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
            (REMOTE / "status").write_text("done")
            shutil.move(str(task_file), str(INBOX / task_file.name))

            # גיבוי
            backup = PROCESSED / task_file.name
            backup.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

            log(f"✓ {task_file.name} -> {result['verdict']}")

        except Exception as e:
            log(f"! Error {task_file}: {e}")

    time.sleep(3)
