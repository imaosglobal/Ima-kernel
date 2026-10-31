import os
from playwright.sync_api import sync_playwright

SITE = os.environ.get("SITE", "https://imaosglobal.github.io/Ima-kernel/")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 390, "height": 844}, locale="en-US")
    page.goto(SITE, wait_until="networkidle", timeout=60000)
    page.wait_for_selector("#root", timeout=15000)
    page.wait_for_selector("button.install-button", timeout=15000)
    assert page.locator("button.install-button").first.is_visible(), "Install IMA button is not visible"
    assert page.get_by_text("Open IMA now", exact=True).count() >= 1, "Open IMA now CTA missing"
    assert page.get_by_text("Talk to IMA", exact=True).count() >= 1, "Talk to IMA CTA missing"
    brand = page.locator("a.brand").first
    href = brand.get_attribute("href") or ""
    assert "utm_source=google" in href and "utm_medium=cpc" in href and "utm_campaign=ima_initial_100ils" in href, "Brand campaign destination missing"
    page.locator(".google-entry").first.wait_for(state="visible", timeout=15000)
    google_frames = page.locator(".google-entry iframe")
    assert google_frames.count() >= 1, "Official Google Identity Services button did not render"
    assert google_frames.first.is_visible(), "Official Google Identity Services button is not visible"
    print("IMA_BROWSER_SMOKE=PASS")
    browser.close()
