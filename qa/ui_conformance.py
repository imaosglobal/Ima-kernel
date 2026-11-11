#!/usr/bin/env python3
"""Dependency-light conformance checks for the IMA public UI."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / "ima-ui/src/App.jsx").read_text(encoding="utf-8")
MAIN = (ROOT / "ima-ui/src/main.jsx").read_text(encoding="utf-8")
INDEX = (ROOT / "ima-ui/index.html").read_text(encoding="utf-8")
COORD = (ROOT / "ima-ui/src/services/updateCoordinator.js").read_text(encoding="utf-8")
SW = (ROOT / "ima-ui/public/sw.js").read_text(encoding="utf-8") if (ROOT / "ima-ui/public/sw.js").exists() else (ROOT / "sw.js").read_text(encoding="utf-8")

checks = {
    "landing_is_minimal": "hero-new" in APP and "GoogleButton" in APP and "user" in APP,
    "authenticated_navigation": "GoogleButton user={user}" in APP and "loggedIn" not in APP,
    "live_browser_linked": "browser-bridge.html" in APP and "t.browser" in APP,
    "chat_panel_present": "ChatPanel" in APP and 'id="chat"' in APP,
    "chat_runtime_has_no_canned_error": "No canned answer was inserted" not in APP,
    "ota_coordinator_loaded": "startImaUpdatePlane()" in MAIN,
    "ota_metadata_present": 'meta name="ima-build-version"' in INDEX,
    "ota_checks_release_metadata": "version.json" in COORD and "cache: 'no-store'" in COORD,
    "service_worker_update_enabled": "registration.update()" in MAIN and "SKIP_WAITING" in MAIN,
    "service_worker_does_not_pin_release": "isReleaseControl" in SW and "version.json" in SW,
    "store_not_falsely_claimed": "actually purchasable" in APP and "Preparing" in APP,
    "community_not_falsely_claimed": "private/group messaging" not in APP or "Build" in APP,
}

failed = [name for name, ok in checks.items() if not ok]
for name, ok in checks.items():
    print(f"{name}: {'PASS' if ok else 'FAIL'}")
if failed:
    raise SystemExit("UI CONFORMANCE FAILED: " + ", ".join(failed))
print(f"RESULT: PASS ({len(checks)} checks)")
