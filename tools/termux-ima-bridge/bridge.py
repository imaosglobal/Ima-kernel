#!/usr/bin/env python3
import base64, json, os, sys, urllib.request, urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

try:
    import websocket
except ImportError:
    print('Missing websocket-client. Run: pip install websocket-client', file=sys.stderr)
    raise

HOST='127.0.0.1'
PORT=int(os.environ.get('IMA_TERMUX_BRIDGE_PORT','8787'))
CDP=os.environ.get('IMA_CHROME_CDP','http://127.0.0.1:9222').rstrip('/')

def get_json(path):
    with urllib.request.urlopen(CDP+path, timeout=5) as r:
        return json.loads(r.read().decode())

def target():
    pages=[x for x in get_json('/json/list') if x.get('type')=='page']
    if not pages: raise RuntimeError('No Chrome page target found')
    return pages[0]

def cdp(method, params=None):
    t=target()
    ws=websocket.create_connection(t['webSocketDebuggerUrl'], timeout=8, origin='http://localhost')
    try:
        ws.send(json.dumps({'id':1,'method':method,'params':params or {}}))
        while True:
            msg=json.loads(ws.recv())
            if msg.get('id')==1:
                if 'error' in msg: raise RuntimeError(msg['error'].get('message','CDP error'))
                return msg.get('result',{})
    finally: ws.close()

def evaluate(expression):
    return cdp('Runtime.evaluate', {'expression':expression,'returnByValue':True,'awaitPromise':True})

class Handler(BaseHTTPRequestHandler):
    def send_json(self,obj,status=200):
        raw=json.dumps(obj,ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header('Content-Type','application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin','*')
        self.send_header('Access-Control-Allow-Headers','Content-Type')
        self.send_header('Access-Control-Allow-Methods','GET,POST,OPTIONS')
        self.end_headers(); self.wfile.write(raw)
    def do_OPTIONS(self): self.send_json({'ok':True})
    def do_GET(self):
        try:
            if self.path=='/status':
                t=target(); self.send_json({'ok':True,'bridge':'ima-termux','port':PORT,'cdp':CDP,'target':{'id':t.get('id'),'title':t.get('title'),'url':t.get('url')}})
            elif self.path=='/tabs': self.send_json({'ok':True,'tabs':get_json('/json/list')})
            elif self.path=='/screenshot': self.send_json({'ok':True,'mime':'image/png','data':cdp('Page.captureScreenshot',{'format':'png','fromSurface':True})['data']})
            else: self.send_json({'ok':False,'error':'not_found'},404)
        except Exception as e: self.send_json({'ok':False,'error':str(e)},503)
    def do_POST(self):
        try:
            n=int(self.headers.get('Content-Length','0')); body=json.loads(self.rfile.read(n) or b'{}'); path=urllib.parse.urlparse(self.path).path
            if path=='/navigate':
                url=str(body.get('url','')).strip()
                if not url.startswith(('https://','http://')): raise ValueError('url must be http(s)')
                evaluate('location.href='+json.dumps(url)); self.send_json({'ok':True,'url':url})
            elif path=='/eval': self.send_json({'ok':True,'result':evaluate(str(body.get('expression',''))).get('result')})
            elif path=='/click':
                selector=str(body.get('selector','')).strip()
                if not selector: raise ValueError('selector required')
                expr='(()=>{const e=document.querySelector('+json.dumps(selector)+');if(!e)return false;e.scrollIntoView({block:"center",inline:"center"});e.click();return true})()'
                ok=evaluate(expr).get('result',{}).get('value'); self.send_json({'ok':bool(ok),'clicked':bool(ok)})
            elif path=='/type': self.send_json({'ok':True,'result':cdp('Input.insertText',{'text':str(body.get('text',''))})})
            elif path=='/key':
                key=str(body.get('key','')); evaluate('(()=>{const e=document.activeElement;if(!e)return false;e.dispatchEvent(new KeyboardEvent("keydown",{key:'+json.dumps(key)+',bubbles:true}));e.dispatchEvent(new KeyboardEvent("keyup",{key:'+json.dumps(key)+',bubbles:true}));return true})()'); self.send_json({'ok':True,'key':key})
            else: self.send_json({'ok':False,'error':'not_found'},404)
        except Exception as e: self.send_json({'ok':False,'error':str(e)},503)

print('IMA bridge listening on http://127.0.0.1:'+str(PORT),flush=True)
print('Chrome CDP: '+CDP,flush=True)
ThreadingHTTPServer((HOST,PORT),Handler).serve_forever()