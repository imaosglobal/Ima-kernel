"""Prepare lawful, non-spam public distribution artifacts for IMA."""
from __future__ import annotations
import hashlib, json
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/".ima"/"distribution"/"prepared_queue.json"
CONTENT={
    "canonical_message":"One humanity. Many cultures. Shared memory. Shared future.",
    "hebrew_message":"אנושות אחת. תרבויות רבות. זיכרון משותף. עתיד משותף.",
    "link":"https://imaosglobal.github.io/Ima-kernel/culture-of-the-heart.html",
    "purpose":"Introduce IMA and the Culture of the Heart without replacing existing cultures.",
}
def run():
    raw=json.dumps(CONTENT,ensure_ascii=False,sort_keys=True)
    item={
        "schema":"IMA-LAWFUL-DISTRIBUTION-1.0",
        "content_id":hashlib.sha256(raw.encode()).hexdigest()[:20],
        "prepared_at":datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z"),
        "content":CONTENT,
        "channels":[
            {"name":"public_website","status":"PUBLISHED_IN_REPOSITORY"},
            {"name":"github","status":"PUBLISHED_IN_REPOSITORY"},
            {"name":"authorized_social","status":"READY_PENDING_AUTHORIZED_CONNECTION"},
            {"name":"press_and_community","status":"READY_PENDING_AUTHORIZED_OUTREACH"},
            {"name":"education_and_events","status":"READY"},
        ],
        "rules":["lawful","consent_respecting","non_spam","no_impersonation","source_attribution"],
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(item,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(item,ensure_ascii=False,indent=2))
if __name__=="__main__":
    run()
