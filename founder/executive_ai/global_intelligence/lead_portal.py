"""Consent-gated lead intake and optional marketing opt-in portal."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs
import json, html, time, uuid
from founder.executive_ai.global_intelligence.deal_hunter import add_lead, match_leads, build_actions
from founder.executive_ai.global_intelligence.consent_registry import add_contact
PORT=8765
HOST="0.0.0.0"
PAGE='''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>IMA — Find a provider</title><style>body{font-family:system-ui;max-width:620px;margin:40px auto;padding:20px}input,select,textarea,button{width:100%;padding:12px;margin:7px 0;box-sizing:border-box}button{cursor:pointer}label{display:block;margin-top:12px}small{color:#555}</style></head><body><h1>Find a provider</h1><p>Tell us what you need. We may connect you with a relevant provider. Your details are not shared for referral without your explicit agreement.</p><form method="post"><label>What do you need?<textarea name="need" required></textarea></label><label>Category<select name="category"><option>real_estate</option><option>vehicles</option><option>insurance</option><option>travel</option><option>b2b</option><option>software</option><option>equipment</option><option>services</option><option>food</option></select></label><label>Name<input name="name" required></label><label>Email<input type="email" name="email" required></label><label>Phone (optional)<input name="phone"></label><label><input type="checkbox" name="consent" value="yes" required> I explicitly agree that my details may be shared with a relevant provider for this request.</label><label><input type="checkbox" name="marketing_consent" value="yes"> I want to receive relevant commercial offers and updates by email. I can unsubscribe at any time.</label><small>Marketing permission is separate from permission to share your request with a provider.</small><button type="submit">Request a provider</button></form></body></html>'''
class Handler(BaseHTTPRequestHandler):
    def send_page(self,body,status=200,content_type="text/html; charset=utf-8"):
        data=body.encode(); self.send_response(status); self.send_header("Content-Type",content_type); self.send_header("Content-Length",str(len(data))); self.end_headers(); self.wfile.write(data)
    def do_GET(self):
        if self.path=="/health": self.send_page(json.dumps({"ok":True,"service":"ima-lead-portal","test_mode":True}),200,"application/json; charset=utf-8"); return
        self.send_page(PAGE)
    def do_POST(self):
        n=int(self.headers.get("Content-Length","0")); raw=self.rfile.read(n).decode(); q=parse_qs(raw)
        if q.get("test_mode",[""])[0]=="yes":
            self.send_page(json.dumps({"ok":True,"accepted":True,"persisted":False,"message":"TEST_MODE: request reached the public portal; no lead was stored."}),200,"application/json; charset=utf-8"); return
        if q.get("consent",[""])[0]!="yes": self.send_page("<h2>Consent is required.</h2>",400); return
        now=time.time(); category=q.get("category",["general"])[0]; email=q.get("email",[""])[0]
        lead={"lead_id":str(uuid.uuid4()),"need":q.get("need",[""])[0][:2000],"category":category,"name":q.get("name",[""])[0][:200],"email":email[:320],"phone":q.get("phone",[""])[0][:80],"consent":True,"consent_at":now,"source":"IMA lead portal"}
        try:
            add_lead(lead)
            marketing=q.get("marketing_consent",[""])[0]=="yes"
            if marketing:
                add_contact({"email":email,"name":lead["name"],"categories":[category],"marketing_consent":True,"consent_at":now,"consent_version":"2026-09-17-v1","consent_text":"I want to receive relevant commercial offers and updates by email. I can unsubscribe at any time.","source":"IMA lead portal","source_url":"public lead portal"})
            matches=match_leads(); build_actions(matches)
            self.send_page("<h2>Request received.</h2><p>Your referral consent was recorded."+(" Your email marketing permission was also recorded." if marketing else "")+"</p>")
        except Exception as exc: self.send_page("<h2>Could not record request.</h2><p>"+html.escape(str(exc))+"</p>",500)
    def log_message(self,*args): pass

def run():
    print(f"LEAD_PORTAL http://0.0.0.0:{PORT}"); ThreadingHTTPServer((HOST,PORT),Handler).serve_forever()
if __name__=="__main__": run()
