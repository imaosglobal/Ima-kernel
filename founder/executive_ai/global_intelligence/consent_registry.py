"""Consent registry for lawful, auditable marketing and referral matching."""
from __future__ import annotations
import hashlib, json, re, time, uuid
from pathlib import Path
ROOT = Path("founder/data")
CONTACTS = ROOT / "approved_mailing_contacts.json"
SUPPRESSION = ROOT / "mailing_suppression.json"
CONSENT_VERSION = "2026-09-17-v1"

def _load(path):
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
    except Exception:
        return []

def _save(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

def normalize_email(email):
    return str(email or "").strip().lower()

def add_contact(contact):
    """Register only explicit, purpose-specific marketing consent."""
    email = normalize_email(contact.get("email"))
    if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
        raise ValueError("valid email is required")
    if contact.get("marketing_consent") is not True:
        raise ValueError("explicit marketing consent is required")
    now = time.time()
    record = {
        "contact_id": contact.get("contact_id") or str(uuid.uuid4()),
        "email": email,
        "name": str(contact.get("name", ""))[:200],
        "categories": sorted(set(contact.get("categories") or [])),
        "consent": True,
        "consent_type": "explicit_marketing_opt_in",
        "consent_at": float(contact.get("consent_at") or now),
        "consent_version": contact.get("consent_version") or CONSENT_VERSION,
        "consent_text": str(contact.get("consent_text", ""))[:2000],
        "source": str(contact.get("source", "IMA lead portal"))[:500],
        "source_url": str(contact.get("source_url", ""))[:1000],
        "status": "active",
        "created_at": now,
        "updated_at": now,
    }
    rows = _load(CONTACTS)
    rows = [r for r in rows if normalize_email(r.get("email")) != email]
    rows.append(record)
    _save(CONTACTS, rows)
    return record

def revoke(email, reason="unsubscribe"):
    email = normalize_email(email)
    rows = _load(CONTACTS)
    changed = False
    now = time.time()
    for r in rows:
        if normalize_email(r.get("email")) == email:
            r["status"] = "unsubscribed"
            r["consent"] = False
            r["updated_at"] = now
            changed = True
    suppressed = _load(SUPPRESSION)
    if not any(normalize_email(x.get("email")) == email for x in suppressed):
        suppressed.append({"email": email, "reason": reason, "at": now})
    _save(CONTACTS, rows)
    _save(SUPPRESSION, suppressed)
    return changed

def eligible(email):
    email = normalize_email(email)
    if any(normalize_email(x.get("email")) == email for x in _load(SUPPRESSION)):
        return False
    return any(normalize_email(x.get("email")) == email and
               x.get("consent") is True and x.get("status") == "active"
               for x in _load(CONTACTS))

def list_active(category=None):
    out=[]
    for r in _load(CONTACTS):
        if r.get("consent") is not True or r.get("status") != "active": continue
        if category and category not in r.get("categories", []): continue
        if not eligible(r.get("email")): continue
        out.append(r)
    return out

def match(need, category=None, limit=50):
    words={w for w in re.findall(r"[a-z0-9]{4,}", str(need).lower())}
    ranked=[]
    for r in list_active(category):
        score=0
        cats=set(r.get("categories", []))
        if category and category in cats: score += 60
        text=" ".join(cats).lower()
        score += min(40, sum(w in text for w in words)*10)
        if score: ranked.append({"contact_id":r["contact_id"],"email":r["email"],"name":r.get("name",""),"score":min(100,score)})
    ranked.sort(key=lambda x:x["score"], reverse=True)
    return ranked[:limit]

def status():
    rows=_load(CONTACTS)
    return {"active":len(list_active()),"total_records":len(rows),"suppressed":len(_load(SUPPRESSION)),"consent_version":CONSENT_VERSION}

def fingerprint(email):
    return hashlib.sha256(normalize_email(email).encode()).hexdigest()[:16]
