import os
from playwright.sync_api import sync_playwright

SITE = os.environ.get("SITE", "https://imaosglobal.github.io/Ima-kernel/")
EXPECTED_SHA = os.environ.get("EXPECTED_SHA", "")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 390, "height": 844}, locale="en-US")
    console_errors = []
    page_errors = []
    page.on("console", lambda m: console_errors.append(f"{m.text} @ {m.location}") if m.type == "error" else None)
    page.on("pageerror", lambda e: page_errors.append(f"{e}\n{getattr(e, 'stack', '')}"))
    def verify_index(url, label):
        response = page.goto(url, wait_until="networkidle", timeout=60000)
        try:
            assert response and response.status == 200, f"{label} index HTTP {response.status if response else None}"
            page.wait_for_selector("#root", state="attached", timeout=15000)
            marker = page.locator('meta[name="ima-build-version"]').get_attribute("content")
            assert EXPECTED_SHA and marker == EXPECTED_SHA, f"{label} build marker mismatch: {marker!r} != {EXPECTED_SHA!r}"
            assert page.locator("#root").inner_text(timeout=2000), f"{label} React root remained empty"
            return marker
        except Exception:
            print("BROWSER_DIAGNOSTIC_LABEL=", label)
            print("BROWSER_DIAGNOSTIC_URL=", page.url)
            print("BROWSER_DIAGNOSTIC_STATUS=", response.status if response else None)
            print("BROWSER_CONSOLE_ERRORS=", console_errors)
            print("BROWSER_PAGE_ERRORS=", page_errors)
            print("BROWSER_HTML_HEAD=", page.content()[:6000])
            raise

    normal_marker = verify_index(SITE, "normal")
    cache_busted_url = SITE + ("&" if "?" in SITE else "?") + "ima-smoke=" + EXPECTED_SHA
    cache_busted_marker = verify_index(cache_busted_url, "cache-busted")
    assert normal_marker == cache_busted_marker, "normal and cache-busted public index versions differ"
    page.wait_for_timeout(1000)
    assert not page_errors, f"browser runtime errors: {page_errors}"
    page.wait_for_selector("button.install-button", timeout=15000)
    assert page.locator("button.install-button").first.is_visible(), "Install IMA button is not visible"
    assert page.get_by_text("Open IMA now", exact=True).count() >= 1, "Open IMA now CTA missing"
    assert page.get_by_text("Talk to IMA", exact=True).count() >= 1, "Talk to IMA CTA missing"
    brand = page.locator("a.brand").first
    href = brand.get_attribute("href") or ""
    assert "utm_source=google" in href and "utm_medium=cpc" in href and "utm_campaign=ima_initial_100ils" in href and "utm_content=ima_logo" in href, "Brand campaign destination missing"
    page.locator(".google-entry").first.wait_for(state="visible", timeout=15000)
    google_root = page.locator(".google-entry > div").first
    assert google_root.count() == 1, "Google Identity Services mount point missing"
    page.wait_for_function("() => !!window.google?.accounts?.id", timeout=15000)
    assert google_root.inner_html().strip(), "Official Google Identity Services button did not render into its mount point"
    print("IMA_BROWSER_SMOKE=PASS")
    browser.close()
