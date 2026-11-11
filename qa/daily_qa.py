#!/usr/bin/env python3
import json, re, sys, time, urllib.parse, urllib.request

BASE="https://imaosglobal.github.io/Ima-kernel/"
API="https://ima-915m.onrender.com"
failures=[]

def get(url, timeout=30):
    req=urllib.request.Request(url, headers={"User-Agent":"IMA-Daily-QA/2.0","Cache-Control":"no-cache"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.geturl(), r.read().decode("utf-8","replace")

def check(name, fn):
    try: fn()
    except Exception as e: failures.append(f"{name}: {e}")

def source_checks():
    app=open("ima-ui/src/App.jsx",encoding="utf-8").read()
    css=open("ima-ui/src/index.css",encoding="utf-8").read()
    manifest=open("ima-ui/public/manifest.json",encoding="utf-8").read()
    index=open("ima-ui/index.html",encoding="utf-8").read()
    assert "renderButton" in app and 'id="ima-google-button"' in app, "Google Identity Services entry missing"
    assert app.count('id="ima-google-button"') == 1, "Google mount duplicated in canonical source"
    assert "MamaFigure" in app and "ChatPanel" in app and "chat-only-panel" in app, "Mama/chat contracts missing"
    assert "SUPPORT_URL" in app and "PRIVACY_URL" in app and "feedback-panel" in app, "support/privacy/feedback contracts missing"
    assert "beforeinstallprompt" in app and "install-button" in app, "PWA install contract missing"
    assert "campaignId=24409551537" in app, "canonical campaign attribution missing"
    assert "overflow-wrap" in css or "word-break" in css, "text overflow protection missing"
    assert "prefers-reduced-motion" in css, "reduced-motion contract missing"
    assert "min-width:0" in css.replace(" ",""), "min-width guard missing"
    assert "ima-192.svg" in manifest and "ima-512.svg" in manifest and "?chat=1" in manifest, "PWA manifest/chat shortcut missing"
    assert '__IMA_BUILD_VERSION__' in index, "public build marker missing"
    assert 'accounts.google.com/gsi/client' in index, "Google GIS script missing"

def public_checks():
    PUBLIC_PAGES_RETRY=3
    last=None
    for attempt in range(PUBLIC_PAGES_RETRY):
        try:
            status,_,html=get(BASE+"?qa=daily")
            if status==200:
                break
            last=f"HTTP {status}"
        except Exception as e:
            last=str(e)
        if attempt < PUBLIC_PAGES_RETRY-1:
            time.sleep(2)
    else:
        raise RuntimeError(f"GitHub Pages retry exhausted: {last}")
    assert status==200, f"public index HTTP {status}"
    assert 'id="root"' in html and 'assets/index-' in html, "canonical React build missing"
    assert 'meta name="ima-build-version"' in html, "public build marker missing"
    for path in ("manifest.json","support.html","privacy.html","feedback.html","icons/ima-192.svg","icons/ima-512.svg"):
        s,_,_=get(BASE+path)
        assert s==200, f"{path}: HTTP {s}"

def api_checks():
    s,_,h=get(API+"/health"); assert s==200, f"health HTTP {s}"
    d=json.loads(h); assert d.get("status")=="ok", f"health payload {d}"
    s,_,h=get(API+"/ima-api/auth/config"); assert s==200, f"auth/config HTTP {s}"
    d=json.loads(h); g=d.get("google",{})
    assert g.get("enabled") and g.get("client_id"), "Google auth is not fully configured"

check("source-contracts",source_checks)
check("public-runtime",public_checks)
check("runtime-auth",api_checks)
if failures:
    print("IMA DAILY QA FAILED")
    print("\n".join("- "+x for x in failures))
    sys.exit(1)
print("IMA DAILY QA PASSED")
