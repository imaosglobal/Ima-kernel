#!/usr/bin/env python3
"""
IMA-Muse Bridge Agent V3
קורא את result מה-daemon ומציג למשתמש לאישור
"""
import json, pathlib, time
BASE = pathlib.Path.home() / "Ima-kernel/.ima"
RESULT = BASE / "remote/result"
STATUS = BASE / "remote/status"
CONSENT_LOG = BASE / "remote/consent_log.jsonl"

def load_result():
    if not RESULT.exists():
        return None
    return json.loads(RESULT.read_text(encoding="utf-8"))

def display_opportunity():
    data = load_result()
    if not data:
        print("⏳ No result yet - waiting for daemon...")
        return None

    opp = data.get("cleaned_opportunity", {})
    print("\n" + "="*60)
    print("🎯 NEW OPPORTUNITY - NEEDS YOUR APPROVAL")
    print("="*60)
    print(f"📌 Title: {opp.get('title')}")
    print(f"🔗 URL: {opp.get('url')}")
    print(f"📂 Category: {opp.get('category')}")
    print(f"\n📝 Signal:\n{opp.get('signal')}\n")
    print(f"⚖️ Verdict: {data.get('verdict')}")
    print(f"🔒 Safety: consent_required={data.get('safety',{}).get('consent_required')}")
    print(f"⛔ Blocked: {data.get('safety',{}).get('blocked')}")
    print("="*60)
    return data

def request_consent(data):
    print("\nOptions:")
    print("[A] Approve - allow next step (e.g., show TOS, open browser)")
    print("[R] Reject - archive and skip")
    print("[Q] Quit")
    choice = input("\nYour choice (A/R/Q): ").strip().lower()

    log_entry = {
        "task_id": data.get("task_id"),
        "timestamp": time.time(),
        "choice": choice,
        "opportunity": data.get("cleaned_opportunity")
    }
    with open(CONSENT_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False)+"\n")

    if choice == "a":
        print("\n✅ APPROVED - You can now manually verify TOS at:", data["cleaned_opportunity"]["url"])
        print("Next: Open https://www.referr.co.uk/terms manually")
        (BASE / "remote/status").write_text("approved")
    elif choice == "r":
        print("\n❌ REJECTED - archived")
        (BASE / "remote/status").write_text("rejected")
    else:
        print("\n⏸️ No action taken")

    return choice

if __name__ == "__main__":
    data = display_opportunity()
    if data:
        request_consent(data)
