#!/usr/bin/env python3
"""LIVE-001 canonical contract gate.

Runs on every CI build and verifies that the public IMA browser surface has
not silently drifted into a duplicate, broken, or insecure configuration.
"""

from __future__ import annotations
import json
import os
import pathlib
import sys
import urllib.request
import urllib.error

ROOT = pathlib.Path(__file__).resolve().parents[1]
failures = []

def fail(msg: str) -> None:
    failures.append(msg)

def read(rel: str) -> str:
    p = ROOT / rel
    if not p.exists():
        fail(f"missing required file: {rel}")
        return ""
    return p.read_text(encoding="utf-8")

# Canonical package.
plugin_raw = read("plugins/ima-chatgpt/plugin.json")
mcp_raw = read("plugins/ima-chatgpt/mcp.json")
submission_raw = read("plugins/ima-chatgpt/chatgpt-app-submission.json")
action_raw = read("services/ima-action-mcp/server/index.mjs")
widget_raw = read("services/ima-action-mcp/widget.html")
browserglass_docker = read("tools/ima-browserglass/Dockerfile")
device_bridge_raw = read("app.py")
trust_wonder_raw = read("governance/IMA_TRUST_WONDER_CORE.md")
wonder_help_raw = read("governance/IMA_WONDER_TO_HELP_CORE.md")
wonder_help_runtime = read("core/wonder_to_help.py")
compound_growth_raw = read("governance/IMA_COMPOUND_GROWTH_CORE.md")
compound_growth_runtime = read("core/compound_growth.py")
adaptive_eligibility_raw = read("governance/IMA_ADAPTIVE_ELIGIBILITY_CORE.md")
adaptive_eligibility_runtime = read("core/adaptive_eligibility.py")
master_runtime_raw = read("ima_master_runtime.py")

try:
    plugin = json.loads(plugin_raw)
except Exception as exc:
    plugin = {}
    fail(f"plugin.json is invalid JSON: {exc}")

try:
    mcp = json.loads(mcp_raw)
except Exception as exc:
    mcp = {}
    fail(f".mcp.json is invalid JSON: {exc}")

try:
    submission = json.loads(submission_raw)
except Exception as exc:
    submission = {}
    fail(f"chatgpt-app-submission.json is invalid JSON: {exc}")

if "AE-001" not in adaptive_eligibility_raw:
    fail("canonical IMA Adaptive Eligibility contract AE-001 is missing")
if 'VERSION = "AE-001-runtime-v1.0"' not in adaptive_eligibility_runtime:
    fail("executable AE-001 runtime layer is missing")
if "build_adaptive_eligibility_context" not in master_runtime_raw or "adaptive_eligibility_context" not in master_runtime_raw:
    fail("canonical master runtime must execute the AE-001 behavior layer")
if "adaptive_eligibility_contract" not in master_runtime_raw:
    fail("master runtime must expose AE-001 runtime state for verification")

# Execute the adaptive layer itself.
try:
    sys.path.insert(0, str(ROOT))
    from core.adaptive_eligibility import assess, build_context as adaptive_context, contract as adaptive_contract_fn
    decision = assess({"language": "he", "consent": True}, {"language": "he"}, {"chat": True}, domain="public")
    if decision.get("status") != "eligible_if_verified":
        fail("AE-001 should keep missing consent explicitly unverified")
    if "adapt" not in adaptive_context("payment route").lower():
        fail("AE-001 executable context missing adaptation behavior")
    if adaptive_contract_fn().get("status") != "implemented_in_canonical_master_runtime":
        fail("AE-001 runtime contract status is not implemented")
except Exception as exc:
    fail(f"AE-001 executable runtime test failed: {exc}")

if "TW-001" not in trust_wonder_raw:
    fail("canonical IMA Trust & Wonder contract TW-001 is missing")
if "get_ima_trust_wonder" not in action_raw:
    fail("Action Core must expose the canonical Trust & Wonder contract")
if "WH-001" not in wonder_help_raw:
    fail("canonical IMA Wonder-to-Help contract WH-001 is missing")
if "get_ima_wonder_to_help" not in action_raw:
    fail("Action Core must expose the canonical Wonder-to-Help contract")
if "VERSION = \"WH-001-runtime-v1.0\"" not in wonder_help_runtime:
    fail("executable WH-001 runtime layer is missing")
if "build_wonder_help_context" not in master_runtime_raw or "wonder_help_context" not in master_runtime_raw:
    fail("canonical master runtime must execute the WH-001 behavior layer")
if "wonder_to_help_contract" not in master_runtime_raw:
    fail("master runtime must expose WH-001 runtime state for verification")

# Execute the behavior layer itself, not only static string checks.
try:
    from core.wonder_to_help import assess_mode, build_context, contract as wonder_help_contract_fn
    if assess_mode("יש לי מצב חירום עכשיו") != "survival":
        fail("WH-001 mode detection regression: survival")
    if assess_mode("אני רוצה לכתוב שיר") != "creation":
        fail("WH-001 mode detection regression: creation")
    runtime_context = build_context("אני לא מבין מה קורה")
    for required in ("Practical help is mandatory", "Never fabricate facts", "Preserve user agency"):
        if required not in runtime_context:
            fail(f"WH-001 executable context missing: {required}")
    if wonder_help_contract_fn().get("status") != "implemented_in_canonical_master_runtime":
        fail("WH-001 runtime contract status is not implemented")
except Exception as exc:
    fail(f"WH-001 executable runtime test failed: {exc}")

if plugin.get("name") != "ima":
    fail("plugin name must remain 'ima'")
if not str(plugin.get("version", "")).strip():
    fail("plugin version missing")
if plugin.get("mcpServers") != "./.mcp.json":
    fail("plugin must reference the canonical .mcp.json")

server = mcp.get("mcpServers", {}).get("ima", {})
endpoint = server.get("url")
if endpoint != "https://ima-universal-action-core.onrender.com/mcp":
    fail(f"canonical MCP endpoint drifted: {endpoint!r}")

interface = plugin.get("extensions", {}).get("com.openai", {}).get("interface", {})
for key in ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"):
    value = interface.get(key, "")
    if not (isinstance(value, str) and value.startswith("https://")):
        fail(f"{key} must be an HTTPS URL")

review = plugin.get("extensions", {}).get("com.openai", {}).get("review", {}).get("test_cases", {})
if len(review.get("positive", [])) != 5:
    fail("plugin review must contain exactly five positive cases")
if len(review.get("negative", [])) != 3:
    fail("plugin review must contain exactly three negative cases")

tool = submission.get("tools", {}).get("ima_live_browser", {})
annotations = tool.get("annotations", {})
for key in ("readOnlyHint", "openWorldHint", "destructiveHint"):
    if key not in annotations:
        fail(f"MCP annotation missing: {key}")

# Canonical server/tool/UI invariants.
required_action_fragments = [
    "registerTool('ima_live_browser'",
    "ui://ima/live-browser/v2.html",
    "registerAppResource",
    "authorizedSessionRequired",
]
for fragment in required_action_fragments:
    if fragment not in action_raw:
        fail(f"Action Core invariant missing: {fragment}")

if "https://ima-browserglass.onrender.com/" not in widget_raw:
    fail("BrowserGlass widget must use the canonical BrowserGlass service")

# Full Android device-screen channel must remain part of LIVE-001, not browser-only.
termux_bridge_raw = read("tools/termux-ima-bridge/bridge.py")
termux_start_raw = read("tools/termux-ima-bridge/start-ima-bridge.sh")
browser_bridge_ui_raw = read("ima-ui/public/browser-bridge.html")
if "device_screen" not in termux_bridge_raw or "/device-screen" not in termux_bridge_raw:
    fail("LIVE-001 full Android device-screen channel is missing from the Termux bridge")
if "ADB_MDNS_AUTO_CONNECT" not in termux_start_raw:
    fail("LIVE-001 Android bridge must auto-discover the paired ADB transport")
if "deviceScreen" not in browser_bridge_ui_raw or "/device-screen" not in browser_bridge_ui_raw:
    fail("LIVE-001 browser bridge UI must expose the full Android device screen")

if "BGLS_CHROME_PATH=/usr/bin/google-chrome-stable" not in browserglass_docker:
    fail("BrowserGlass must pin a deterministic Chrome binary")
if "git clone --depth 1 https://github.com/psmux/browserglass.git" not in browserglass_docker:
    fail("BrowserGlass build source is missing")

for fragment in (
    '@app.post("/ima-api/device/register")',
    '@app.get("/ima-api/device/poll")',
    '@app.post("/ima-api/device/result")',
    '@app.post("/ima-api/device/mcp-command")',
):
    if fragment not in device_bridge_raw:
        fail(f"device bridge invariant missing: {fragment}")

# Duplicate plugin names in repository packages are a release blocker.
for p in (ROOT / "plugins").rglob("plugin.json"):
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        continue
    if data.get("name") == "ima" and p != ROOT / "plugins/ima-chatgpt/plugin.json":
        fail(f"duplicate canonical IMA plugin manifest: {p.relative_to(ROOT)}")

# Optional live smoke test. CI runs this by default; local runs can skip it.
if os.environ.get("IMA_SKIP_LIVE_SMOKE") != "1":
    for url in (
        "https://ima-universal-action-core.onrender.com/health",
        "https://ima-browserglass.onrender.com/healthz",
    ):
        last_error = None
        for attempt, timeout in enumerate((20, 30, 45), start=1):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "IMA-LIVE-001-CI/1.0"})
                with urllib.request.urlopen(req, timeout=timeout) as response:
                    if response.status == 200:
                        last_error = None
                        break
                    last_error = f"HTTP {response.status}"
            except Exception as exc:
                last_error = str(exc)
            if attempt < 3:
                import time
                time.sleep(2 * attempt)
        if last_error:
            fail(f"live health check failed after retries: {url} -> {last_error}")

if failures:
    print("LIVE-001 GATE: FAIL")
    for item in failures:
        print(" -", item)
    sys.exit(1)

print("LIVE-001 GATE: PASS")
print("Canonical IMA plugin, MCP endpoint, BrowserGlass, device bridge, Trust & Wonder contracts and executable WH-001 behavior layer are consistent.")

assert "AE-001" in adaptive_eligibility_raw
assert "AE-001-runtime-v1.0" in adaptive_eligibility_runtime
assert "CG-001" in compound_growth_raw
assert "COMPOUND-GROWTH" in compound_growth_runtime
assert "notice → capture lesson → validate → improve → test → verify" in compound_growth_raw
assert "truth_safety_privacy_or_agency" in compound_growth_runtime

assert "<<<<<<<" not in read(".ima/loop/UNIFIED_LOOP_STATE.json")
assert "=======" not in read(".ima/loop/UNIFIED_LOOP_STATE.json")
assert ">>>>>>>" not in read(".ima/loop/UNIFIED_LOOP_STATE.json")
assert "CG-001" in read("docs/IMA_CANONICAL_UNIFICATION_LEDGER_2026-11-13.md")
assert "Single canonical runtime" in read("docs/IMA_CANONICAL_UNIFICATION_LEDGER_2026-11-13.md")
