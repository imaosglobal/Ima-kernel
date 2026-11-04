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
    page.on("pageerror", lambda e: page_errors.append(str(e)))
    page.add_init_script("""
        window.__imaRuntimeErrors = [];
        window.addEventListener('error', event => window.__imaRuntimeErrors.push({
            message: event.message, filename: event.filename, line: event.lineno,
            column: event.colno, stack: event.error?.stack || ''
        }));
        window.addEventListener('unhandledrejection', event => window.__imaRuntimeErrors.push({
            message: String(event.reason?.message || event.reason),
            stack: event.reason?.stack || ''
        }));
    """)
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
            try:
                print("BROWSER_RUNTIME_ERRORS=", page.evaluate("() => window.__imaRuntimeErrors || []"))
            except Exception as diagnostic_error:
                print("BROWSER_RUNTIME_ERRORS_UNAVAILABLE=", str(diagnostic_error))
            print("BROWSER_HTML_HEAD=", page.content()[:6000])
            raise

    normal_marker = verify_index(SITE, "normal")
    cache_busted_url = SITE + ("&" if "?" in SITE else "?") + "ima-smoke=" + EXPECTED_SHA
    cache_busted_marker = verify_index(cache_busted_url, "cache-busted")
    assert normal_marker == cache_busted_marker, "normal and cache-busted public index versions differ"

    def verify_navigation(width):
        page.set_viewport_size({"width": width, "height": 844})
        page.wait_for_timeout(150)
        nav = page.locator(".topbar nav")
        assert nav.is_visible(), f"Navigation is not visible at {width}px"
        nav_metrics = nav.evaluate("(el) => ({clientWidth: el.clientWidth, scrollWidth: el.scrollWidth, overflowX: getComputedStyle(el).overflowX})")
        if width <= 850:
            assert nav_metrics["overflowX"] in ("auto", "scroll"), f"Mobile navigation is not horizontally scrollable at {width}px: {nav_metrics}"
        buttons = nav.locator("button")
        assert buttons.count() == 8, f"Expected 8 navigation controls at {width}px, found {buttons.count()}"
        for index in range(buttons.count()):
            metrics = buttons.nth(index).evaluate("(el) => ({whiteSpace: getComputedStyle(el).whiteSpace, flexShrink: getComputedStyle(el).flexShrink, scrollWidth: el.scrollWidth, clientWidth: el.clientWidth})")
            assert metrics["whiteSpace"] == "nowrap", f"Navigation label {index} wraps at {width}px: {metrics}"
            assert metrics["flexShrink"] == "0", f"Navigation control {index} shrinks at {width}px: {metrics}"
            assert metrics["scrollWidth"] <= metrics["clientWidth"] + 1, f"Navigation label {index} overflows its own button at {width}px: {metrics}"
        if width <= 400:
            assert nav_metrics["scrollWidth"] > nav_metrics["clientWidth"], f"390px navigation should expose horizontal scrolling: {nav_metrics}"

    for viewport_width in (390, 768, 1280):
        verify_navigation(viewport_width)
    page.set_viewport_size({"width": 390, "height": 844})
    page.wait_for_timeout(1000)
    assert not page_errors, f"browser runtime errors: {page_errors}"
    page.wait_for_selector("button.install-button", timeout=15000)
    assert page.locator("button.install-button").first.is_visible(), "Install IMA button is not visible"
    assert page.get_by_text("Open IMA now", exact=True).count() >= 1, "Open IMA now CTA missing"
    brand = page.locator("a.brand").first
    href = brand.get_attribute("href") or ""
    assert "ads.google.com/aw/campaigns" in href and "campaignId=24409551537" in href, "Brand Google Ads campaign destination missing"
    hero_campaign = page.locator("a.avatar-campaign-link").first
    hero_href = hero_campaign.get_attribute("href") or ""
    assert "ads.google.com/aw/campaigns" in hero_href and "campaignId=24409551537" in hero_href, "Hero image does not link to the Google Ads campaign"
    assert page.locator("a.skip-link").count() == 0, "Skip to IMA link must stay removed"
    below = page.locator(".hero-below-image-actions").first
    assert below.is_visible(), "Hero controls container missing"
    assert below.locator(".google-entry").count() == 1, "Google sign-in must be directly below the hero image"
    assert below.locator("button.install-button").count() == 1, "Install/home-screen control must be directly below the hero image"
    assert page.locator(".personalization-panel").count() == 0, "nonfunctional personalization panel must stay removed"
    logo = page.locator(".clean-ima-logo").first
    assert logo.is_visible(), "clean IMA logo hero is missing"
    assert "f057cd08143342f2994f85d847572fa8" in (logo.get_attribute("src") or ""), "clean canonical IMA logo asset mismatch"
    assert page.locator(".hero-avatar canvas").count() == 0, "legacy character render must not return to the public hero"
    page.locator(".google-entry").first.wait_for(state="visible", timeout=15000)
    google_roots = page.locator(".google-entry")
    assert google_roots.count() == 1, f"Expected exactly one Google login control, found {google_roots.count()}"
    page.wait_for_function("() => !!window.google?.accounts?.id", timeout=15000)
    google_root = page.locator(".google-entry > div").first
    assert google_root.inner_html().strip(), "Official Google Identity Services button did not render into its mount point"
    assert page.locator("iframe[src*='accounts.google.com']").count() <= 1, "Duplicate Google GIS iframe detected"
    for path in ["/manifest.json", "/support.html", "/privacy.html", "/feedback.html"]:
        rr = page.request.get(SITE.rstrip("/") + path)
        assert rr.ok, f"Public artifact missing: {path} ({rr.status})"
    print("IMA_BROWSER_SMOKE=PASS")
    browser.close()
