import os
from playwright.sync_api import sync_playwright

SITE = os.environ.get("SITE", "https://imaosglobal.github.io/Ima-kernel/")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 390, "height": 844}, locale="en-US")
    console_errors = []
    page_errors = []
    page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: page_errors.append(str(e)))
    response = page.goto(SITE, wait_until="networkidle", timeout=60000)
    try:
        page.wait_for_selector("#root", state="attached", timeout=15000)
    except Exception:
        print("BROWSER_DIAGNOSTIC_URL=", page.url)
        print("BROWSER_DIAGNOSTIC_STATUS=", response.status if response else None)
        print("BROWSER_CONSOLE_ERRORS=", console_errors)
        print("BROWSER_PAGE_ERRORS=", page_errors)
        print("BROWSER_HTML_HEAD=", page.content()[:6000])
        raise
    page.wait_for_timeout(3000)
    if not page.locator("#root").inner_text(timeout=2000):
        print("BROWSER_DIAGNOSTIC_URL=", page.url)
        print("BROWSER_DIAGNOSTIC_STATUS=", response.status if response else None)
        print("BROWSER_CONSOLE_ERRORS=", console_errors)
        print("BROWSER_PAGE_ERRORS=", page_errors)
        print("BROWSER_HTML_HEAD=", page.locator("body").inner_html(timeout=2000)[:4000])
        raise AssertionError("IMA React root remained empty")
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
