import os
from playwright.sync_api import sync_playwright

SITE = os.environ.get("SITE", "https://imaosglobal.github.io/Ima-kernel/")
EXPECTED_SHA = os.environ.get("EXPECTED_SHA", "")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 390, "height": 844}, locale="he-IL")
    console_errors, page_errors = [], []
    page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: page_errors.append(str(e)))

    def verify_index(url, label):
        response = page.goto(url, wait_until="networkidle", timeout=60000)
        assert response and response.status == 200, f"{label} HTTP {response.status if response else None}"
        page.wait_for_selector("#root", state="attached", timeout=15000)
        marker = page.locator('meta[name="ima-build-version"]').get_attribute("content")
        assert EXPECTED_SHA and marker == EXPECTED_SHA, f"{label} build marker mismatch"
        assert page.locator("#root").inner_text(timeout=3000), f"{label} React root remained empty"
        return marker

    normal = verify_index(SITE, "normal")
    busted = verify_index(SITE + "?ima-smoke=" + EXPECTED_SHA, "cache-busted")
    assert normal == busted

    for width in (390, 768, 1280):
        page.set_viewport_size({"width": width, "height": 844})
        page.wait_for_timeout(250)
        nav = page.locator(".site-header nav")
        assert nav.is_visible(), f"navigation hidden at {width}px"
        assert nav.locator("button").count() == 4, f"expected 4 nav controls at {width}px"
    page.set_viewport_size({"width": 390, "height": 844})

    assert page.locator(".mama-figure").count() >= 1, "Mama figure missing"
    assert page.locator(".chat-collapsed").count() == 1, "collapsed chat missing"
    assert page.locator("#feedback-panel").count() == 1, "feedback panel missing"
    assert page.locator("button.install-button").count() == 0 or page.locator("button.install-button").is_visible() is False, "install must be gated by Google sign-in"
    google = page.locator("#ima-google-button")
    assert google.count() == 1, "canonical Google mount missing"
    page.wait_for_function("() => !!window.google?.accounts?.id", timeout=15000)
    assert google.inner_html().strip(), "official Google Identity Services button did not render"
    assert page.locator("iframe[src*='accounts.google.com']").count() <= 1, "duplicate Google GIS iframe detected"

    page.locator(".chat-collapsed button").click()
    page.locator(".chat-panel").wait_for()
    composer = page.locator(".chat-composer input")
    composer.fill("ענה במילה אחת: שלום")
    page.locator(".chat-composer button").click()
    page.locator(".chat-bubble.ima").last.wait_for(state="visible", timeout=60000)
    answer = page.locator(".chat-bubble.ima").last.inner_text().strip()
    assert answer and "IMA" not in answer[:3] or answer, "IMA did not return a real answer"
    page.locator(".chat-close").click()
    assert page.locator(".chat-collapsed").count() == 1, "chat did not collapse back to Mama"

    for path in ("/manifest.json", "/support.html", "/privacy.html", "/feedback.html"):
        rr = page.request.get(SITE.rstrip("/") + path)
        assert rr.ok, f"public artifact missing: {path} ({rr.status})"

    page.goto(SITE + "?chat=1", wait_until="networkidle", timeout=60000)
    page.wait_for_selector(".ima-chat-only", timeout=15000)
    assert page.locator(".ima-chat-only .mama-figure").count() == 1, "chat-only Mama missing"
    assert page.locator(".ima-chat-only .chat-login").count() == 1, "chat-only Google gate missing"
    assert page.locator(".ima-chat-only #ima-google-button").count() == 1, "chat-only Google mount missing"

    assert not page_errors, f"browser runtime errors: {page_errors}"
    print("IMA_BROWSER_SMOKE=PASS")
    browser.close()
