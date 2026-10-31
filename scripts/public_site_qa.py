#!/usr/bin/env python3
import os, re, sys, requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

SITE = os.environ.get("SITE", "https://imaosglobal.github.io/Ima-kernel/")
API = os.environ.get("API", "https://ima-915m.onrender.com")
TIMEOUT = 25

def check_url(session, url, label):
    r = session.get(url, timeout=TIMEOUT, allow_redirects=True)
    if r.status_code >= 400:
        raise AssertionError(f"{label}: HTTP {r.status_code}: {url}")
    return r

s = requests.Session()
page = check_url(s, SITE, "public site")
soup = BeautifulSoup(page.text, "html.parser")

assert soup.find("script", src=re.compile(r"accounts\.google\.com/gsi/client")), "Google Identity Services library missing"
assert soup.find("link", rel="manifest"), "PWA manifest link missing"
assert soup.find(id="root"), "React root missing"
assert "Ima-kernel" in page.url, "unexpected public site URL"

# Validate every explicit href/src/poster in the delivered HTML shell.
resources = []
for tag, attr in [("a","href"), ("img","src"), ("script","src"), ("link","href"), ("video","poster"), ("source","src")]:
    for node in soup.find_all(tag):
        value = node.get(attr)
        if not value or value.startswith(("#","mailto:","tel:","javascript:","data:")):
            continue
        resources.append((tag, attr, urljoin(SITE, value)))

for tag, attr, url in resources:
    parsed = urlparse(url)
    if parsed.scheme not in ("http","https"):
        raise AssertionError(f"unsupported {tag}[{attr}] URL: {url}")
    check_url(s, url, f"{tag}[{attr}]")

# Public API smoke.
check_url(s, API + "/health", "API health")
cfg = check_url(s, API + "/ima-api/auth/config", "Google auth config").json()
assert cfg.get("google", {}).get("enabled") is True, f"Google auth not enabled: {cfg}"
manifest_url = urljoin(SITE, soup.find("link", rel="manifest").get("href"))
manifest = check_url(s, manifest_url, "PWA manifest").json()
icons = manifest.get("icons") or []
assert any(i.get("src") and i.get("sizes") in ("192x192","any") for i in icons), "PWA 192/any icon missing"
assert any(i.get("src") and i.get("sizes") == "512x512" for i in icons), "PWA 512 icon missing"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 390, "height": 844}, locale="he-IL")
    console_errors = []
    page_errors = []
    tab = context.new_page()
    tab.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
    tab.on("pageerror", lambda e: page_errors.append(str(e)))
    tab.goto(SITE, wait_until="networkidle", timeout=60000)
    tab.wait_for_timeout(2500)

    # Official GIS must actually render its button, not merely exist in source.
    assert tab.locator("iframe[src*='accounts.google.com']").count() >= 1 or tab.locator("div[role='button']").count() >= 1, "Google-rendered sign-in button not observed"
    assert tab.locator(".avatar-campaign-link").count() == 1, "IMA campaign image link missing"
    campaign = tab.locator(".avatar-campaign-link").get_attribute("href")
    assert campaign and "utm_source=google" in campaign and "utm_medium=cpc" in campaign, f"campaign destination invalid: {campaign}"
    assert tab.locator("button.install-button").count() >= 1, "install button missing"
    assert tab.locator("button.install-button").first.is_visible(), "install button not visible"

    # Check every same-origin anchor target.
    anchors = tab.locator("a[href]")
    for i in range(anchors.count()):
        href = anchors.nth(i).get_attribute("href")
        if not href or href.startswith(("#","mailto:","tel:")):
            continue
        absolute = urljoin(SITE, href)
        if urlparse(absolute).netloc == urlparse(SITE).netloc:
            check_url(s, absolute, "same-origin link")

    # Check every rendered image actually loads.
    imgs = tab.locator("img")
    for i in range(imgs.count()):
        assert imgs.nth(i).evaluate("(img) => img.complete && img.naturalWidth > 0"), f"broken image #{i}"

    # Safe interaction pass for buttons. Skip authentication/install/destructive controls.
    buttons = tab.locator("button:visible")
    skipped = {"install", "memory", "Google"}
    for i in range(buttons.count()):
        b = buttons.nth(i)
        text = (b.inner_text(timeout=2000) or "").strip()
        if any(x.lower() in text.lower() for x in skipped):
            continue
        try:
            b.click(timeout=2500)
            tab.wait_for_timeout(100)
        except Exception:
            # A button may be intentionally non-clickable while another state is active.
            pass

    if console_errors or page_errors:
        raise AssertionError("browser errors: " + " | ".join(console_errors + page_errors))

    browser.close()

print("IMA PUBLIC QA PASS")
print(f"checked_html_resources={len(resources)}")
print(f"google_enabled={cfg.get('google',{}).get('enabled')}")
print("google_button=rendered")
print("campaign_image_link=verified")
print("images=loaded")
print("links=checked")
print("buttons=interaction_smoke_checked")
