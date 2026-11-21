import os
from playwright.sync_api import sync_playwright

SITE=os.environ.get("SITE","https://imaosglobal.github.io/Ima-kernel/")
EXPECTED_SHA=os.environ.get("EXPECTED_SHA","")

with sync_playwright() as p:
    browser=p.chromium.launch()
    page=p.new_page(viewport={"width":390,"height":844},locale="he-IL")
    console_errors=[]; page_errors=[]
    page.on("console",lambda m: console_errors.append(m.text) if m.type=="error" else None)
    page.on("pageerror",lambda e: page_errors.append(str(e)))

    def load(url,label):
        r=page.goto(url,wait_until="networkidle",timeout=60000)
        assert r and r.status==200,f"{label} HTTP {r.status if r else None}"
        page.wait_for_selector("#root",state="attached",timeout=15000)
        marker=page.locator('meta[name="ima-build-version"]').get_attribute("content")
        assert EXPECTED_SHA and marker==EXPECTED_SHA,f"{label} build marker mismatch"
        assert page.locator("#root").inner_text(timeout=3000),f"{label} root empty"
        return marker

    assert load(SITE,"normal")==load(SITE+"?ima-smoke="+EXPECTED_SHA,"cache-busted")

    for width in (390,768,1280):
        page.set_viewport_size({"width":width,"height":844}); page.wait_for_timeout(250)
        assert page.locator(".site-header").is_visible(),f"header hidden at {width}px"
        assert page.locator(".hero").is_visible(),f"hero hidden at {width}px"
        assert page.locator(".hero h1").is_visible(),f"hero title hidden at {width}px"
        assert page.locator(".primary").count()>=1,f"primary CTA missing at {width}px"
        assert page.locator(".job-card").count()==4,f"job cards missing at {width}px"

    page.set_viewport_size({"width":390,"height":844})
    assert page.locator(".mama-figure").count()>=1,"Mama identity missing"
    assert page.locator(".chat-bar").count()==0,"chat bar must not appear before sign-in"
    assert page.locator("#ima-google-button").count()==1,"canonical Google mount missing"
    page.wait_for_function("() => !!window.google?.accounts?.id",timeout=15000)
    assert page.locator("#ima-google-button").inner_html().strip(),"official Google button did not render"
    assert page.locator("iframe[src*='accounts.google.com']").count()<=1,"duplicate Google GIS iframe"

    campaign=page.locator(".brand").get_attribute("href")
    assert "campaignId=24409551537" in campaign and "utm_source=google" in campaign,"Google campaign URL missing"

    assert page.locator(".resilience-center").count()==0,"emergency/resilience content must not be on entry page"
    assert page.locator(".canonical-connectors").count()==0,"technical control-room content must not be on entry page"

    # Main content must not visibly overlap at common mobile/tablet/desktop sizes.
    for width in (390,768,1280):
        page.set_viewport_size({"width":width,"height":900}); page.wait_for_timeout(200)
        boxes=page.locator("main > section").evaluate_all("""els => els.map(e => { const r=e.getBoundingClientRect(); return {top:r.top,bottom:r.bottom,left:r.left,right:r.right,height:r.height}; })""")
        for a,b in zip(boxes,boxes[1:]):
            assert b["top"] >= a["bottom"]-1,f"section overlap at {width}px: {a} / {b}"

    for path in ("/manifest.json","/support.html","/privacy.html","/feedback.html"):
        rr=page.request.get(SITE.rstrip("/")+path)
        assert rr.ok,f"public artifact missing: {path} ({rr.status})"

    page.goto(SITE+"?chat=1",wait_until="networkidle",timeout=60000)
    page.wait_for_selector(".chat-only-page",timeout=15000)
    assert page.locator(".chat-only-page #ima-google-button").count()==1,"chat-only Google gate missing"

    assert not page_errors,f"browser runtime errors: {page_errors}"
    print("IMA_BROWSER_SMOKE=PASS")
    browser.close()
