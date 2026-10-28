#!/usr/bin/env python3
"""Source-level public IMA reconciliation for the single canonical loop.

This audit never promotes source presence to VERIFIED_LIVE. Runtime claims require
separate browser/API/deployment evidence.
"""
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / ".ima" / "public_reconciliation" / "state.json"

REQUIRED = {
    "app": ROOT / "ima-ui/src/App.jsx",
    "i18n": ROOT / "ima-ui/src/i18n.js",
    "chat": ROOT / "ima-ui/src/services/imaChat.js",
    "analytics": ROOT / "ima-ui/src/services/analytics.js",
    "capability_registry": ROOT / "docs/IMA_CAPABILITY_REGISTRY.json",
    "requirements": ROOT / "docs/IMA_MASTER_REQUIREMENTS_LEDGER.md",
    "nonprofit": ROOT / "docs/IMA_GLOBAL_NONPROFIT_CHARTER.md",
    "finance": ROOT / "docs/IMA_FINANCIAL_LEDGER_SCHEMA.json",
    "succession": ROOT / "docs/IMA_CREATOR_SUCCESSION_AND_ESTATE.md",
}

def run():
    findings = []
    for name, path in REQUIRED.items():
        findings.append({
            "surface": name,
            "status": "IMPLEMENTED" if path.exists() else "BLOCKED",
            "evidence": str(path.relative_to(ROOT)),
        })

    app = REQUIRED["app"].read_text(encoding="utf-8") if REQUIRED["app"].exists() else ""
    i18n = REQUIRED["i18n"].read_text(encoding="utf-8") if REQUIRED["i18n"].exists() else ""
    checks = {
        "google_identity_flow_present": "GoogleLogin" in app and "signInWithGoogleCredential" in app,
        "chat_entry_present": "askIma(" in app,
        "memory_controls_present": "getMemoryConsent" in app and "memoryScope" in app,
        "accessibility_controls_present": "accessibility" in app and "reduced-motion" in app,
        "rtl_localization_present": "dir:'rtl'" in i18n,
        "community_entry_present": "community" in app,
        "shop_entry_present": "shop" in app,
        "media_entry_present": "watch" in app,
        "install_pwa_entry_present": "beforeinstallprompt" in app,
    }

    record = {
        "schema": "IMA-PUBLIC-RECONCILIATION-1.0",
        "timestamp": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "status": "SOURCE_RECONCILED",
        "runtime_status": "NOT_VERIFIED",
        "truth_rule": "Source code presence is not runtime proof.",
        "findings": findings,
        "checks": checks,
        "next_gate": "browser/API/deployment verification for public runtime",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, ensure_ascii=False, indent=2))
    return 0 if all(x["status"] == "IMPLEMENTED" for x in findings) else 1

if __name__ == "__main__":
    raise SystemExit(run())
