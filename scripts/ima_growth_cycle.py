#!/usr/bin/env python3
"""Canonical IMA growth/readiness cycle.

This script never invents traffic or users. It produces a machine-readable
readiness record from repository capabilities and optional first-party
analytics configuration.
"""
from __future__ import annotations
import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / ".ima" / "growth" / "GLOBAL_GROWTH_STATE.json"

def truth(value: bool, source: str) -> dict:
    return {"available": bool(value), "source": source}

def run() -> dict:
    state = {
        "schema": "IMA-GLOBAL-GROWTH-1.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "principle": "real_users_only",
        "funnel": ["DISCOVER","VISIT","START","RETURN","VALUE","FEEDBACK","IMPROVE","SHARE","RETURN"],
        "analytics": {
            "posthog_configured": truth(bool(os.getenv("POSTHOG_API_KEY")), "runtime environment"),
            "posthog_host_configured": truth(bool(os.getenv("POSTHOG_HOST")), "runtime environment"),
        },
        "distribution": {
            "website": True,
            "pwa": Path(ROOT / "manifest.webmanifest").exists(),
            "android_project": Path(ROOT / "android").exists(),
            "store_listing_verified": False,
            "external_social_authorization": False,
        },
        "self_marketing": {
            "spec_present": Path(ROOT / "docs/IMA_SELF_MARKETING_AND_GROWTH_ENGINE.md").exists(),
            "global_growth_spec_present": Path(ROOT / "docs/IMA_GLOBAL_USER_GROWTH.md").exists(),
            "truth_rule": "marketing claims require evidence; attention is not verified value",
        },
        "feedback": {
            "api_contract": Path(ROOT / "app.py").exists(),
            "public_feedback_page": Path(ROOT / "feedback.html").exists(),
        },
        "localization_target": ["he","en","ar","es","fr","pt","de","hi","ja","ko","zh"],
        "truth_rule": "Unknown metrics remain UNKNOWN; no synthetic users, ratings or reviews.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return state

if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
