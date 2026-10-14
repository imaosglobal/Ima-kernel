#!/usr/bin/env python3
import json, random, re, sys, urllib.parse, urllib.request

BASE="https://imaosglobal.github.io/Ima-kernel/"
API="https://ima-915m.onrender.com"
PAGES=["index.html","human-centered-intelligence.html","compassion.html","global.html","geniza.html"]
failures=[]

def get(url, timeout=20):
    req=urllib.request.Request(url, headers={"User-Agent":"IMA-Daily-QA/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.geturl(), r.read().decode("utf-8","replace")

def check(name, fn):
    try: fn()
    except Exception as e: failures.append(f"{name}: {e}")

def page_checks():
    status, final, html=get(BASE)
    assert status==200, f"HTTP {status}"
    scripts = re.findall(r'<script[^>]+src=["\\\']([^"\\\']+\\.js)["\\\']', html)
    assets = []
    for src in scripts:
        try:
            s, _, js = get(urllib.parse.urljoin(BASE, src))
            if s == 200:
                assets.append(js)
        except Exception:
            pass
    source_app = open("ima-ui/src/App.jsx", encoding="utf-8").read()
    bundle = "\\n".join(assets)
    assert "כניסה עם Google" in source_app, "Google entry missing from canonical UI source"
    assert '<section className="chat-section" id="space">' in source_app, "canonical chat section missing"
    assert 'id="chat"' in source_app and 'className="chat-shell"' in source_app, "canonical chat shell missing"
    assert "אפשר פשוט לדבר עם אמא" not in source_app, "old landing copy still present"
    assert "chat-tools" not in source_app, "stale broken selectors remain"
    assert 'href="#about"' in source_app or 'href="#about"' in html, "Learn-about CTA has no destination"
    assert "google.accounts.id.renderButton" in source_app, "official GIS button rendering missing from canonical UI source"
    for p in PAGES[1:]:
        s,_,h=get(urllib.parse.urljoin(BASE,p))
        assert s==200, f"{p}: HTTP {s}"
        assert "<title>" in h and 'rel="canonical"' in h, f"{p}: SEO metadata incomplete"
        assert 'href="./index.html"' in h, f"{p}: no return path"

def visual_contract_checks():
    css_path = 'ima-ui/src/index.css'
    with open(css_path, encoding='utf-8') as handle:
        css = handle.read()
    assert 'overflow-wrap' in css or 'word-break' in css, 'source CSS: text overflow protection missing'
    assert 'prefers-reduced-motion' in css, 'source CSS: reduced-motion contract missing'
    assert 'min-width:0' in css.replace(' ', ''), 'source CSS: min-width guard missing'
def api_checks():
    s,_,h=get(API+"/health"); assert s==200, f"health HTTP {s}"
    d=json.loads(h); assert d.get("status")=="ok", f"health payload {d}"
    s,_,h=get(API+"/ima-api/auth/config"); assert s==200, f"auth/config HTTP {s}"
    d=json.loads(h); g=d.get("google",{})
    if not g.get("enabled"):
        raise AssertionError("GOOGLE_CLIENT_ID is not configured on Render")
    assert g.get("client_id"), "Google is enabled but client_id is absent"

def monkey_checks():
    urls=[]
    _,_,home=get(BASE)
    for href in re.findall(r'href=["\']([^"\']+)["\']',home):
        if href.startswith("./") and href.endswith(".html"):
            urls.append(urllib.parse.urljoin(BASE,href))
    urls=list(dict.fromkeys(urls))
    random.seed(20261013)
    for url in random.sample(urls, min(len(urls), 10)):
        s,final,_=get(url+"?qa="+str(random.randint(1,999999)))
        assert s==200, f"{url}: HTTP {s}"
        assert urllib.parse.urlparse(final).netloc=="imaosglobal.github.io", f"unexpected host {final}"

check("landing-page",page_checks)
check("runtime-auth",api_checks)
check("visual-contract",visual_contract_checks)
check("monkey-navigation",monkey_checks)
if failures:
    print("IMA DAILY QA FAILED")
    print("\n".join("- "+x for x in failures))
    sys.exit(1)
print("IMA DAILY QA PASSED")
