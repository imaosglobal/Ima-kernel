#!/usr/bin/env python3
import base64, json, os, sys, time, threading, urllib.request, urllib.parse, pathlib, subprocess, socket
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

try:
    import websocket
except ImportError:
    print('Missing websocket-client. Run: pip install websocket-client', file=sys.stderr)
    raise

HOST='127.0.0.1'
PORT=int(os.environ.get('IMA_TERMUX_BRIDGE_PORT','8787'))
CDP=os.environ.get('IMA_CHROME_CDP','http://127.0.0.1:9222').rstrip('/')
TARGET_HINT=os.environ.get('IMA_CHROME_TARGET_HINT','imaosglobal.github.io/Ima-kernel').strip().lower()
CLOUD_API=os.environ.get('IMA_CLOUD_API_BASE','https://ima-915m.onrender.com').rstrip('/')
BROWSERGLASS_API=os.environ.get('IMA_BROWSERGLASS_API','https://ima-browserglass.onrender.com').rstrip('/')
STATE_FILE=os.path.expanduser(os.environ.get('IMA_DEVICE_STATE_FILE','~/.config/ima/device.json'))
def load_device_key():
    if os.environ.get('IMA_DEVICE_KEY','').strip(): return os.environ['IMA_DEVICE_KEY'].strip()
    try: return str(json.loads(pathlib.Path(STATE_FILE).read_text(encoding='utf-8')).get('device_key','')).strip()
    except Exception: return ''
DEVICE_KEY=load_device_key()
CLOUD_POLL_SECONDS=max(1.0,float(os.environ.get('IMA_CLOUD_POLL_SECONDS','2')))
CLOUD_TIMEOUT=max(3.0,float(os.environ.get('IMA_CLOUD_TIMEOUT','12')))
FRAME_UPLOAD_SECONDS=max(1.0,float(os.environ.get('IMA_FRAME_UPLOAD_SECONDS','2')))
LOCAL_EVAL_ENABLED=os.environ.get('IMA_ENABLE_LOCAL_EVAL','0').strip().lower() in ('1','true','yes','on')
ALLOWED_ORIGINS={x.strip().rstrip('/') for x in os.environ.get('IMA_ALLOWED_ORIGINS','https://imaosglobal.github.io,http://localhost:5173,http://127.0.0.1:5173').split(',') if x.strip()}
ACTION_PATHS={'/navigate','/eval','/click','/tap','/scroll','/type','/key'}
ADB_BIN=os.environ.get('IMA_ADB_BIN','/data/data/com.termux/files/usr/bin/adb')
ADB_SERIAL=os.environ.get('IMA_ADB_SERIAL','').strip()

def device_serial():
    env=dict(os.environ); env['ADB_MDNS_AUTO_CONNECT']='adb-tls-connect'
    preferred=ADB_SERIAL
    try:
        subprocess.run([ADB_BIN,'start-server'],env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=8)
    except Exception:
        pass
    try:
        out=subprocess.run([ADB_BIN,'devices'],env=env,capture_output=True,text=True,timeout=5).stdout
        for line in out.splitlines()[1:]:
            parts=line.split()
            if len(parts)>=2 and parts[1]=='device':
                try:
                    subprocess.run([ADB_BIN,'-s',parts[0],'forward','tcp:9222','localabstract:chrome_devtools_remote'],env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=8)
                except Exception:
                    pass
                return parts[0]
    except Exception:
        pass
    if preferred:
        try:
            subprocess.run([ADB_BIN,'connect',preferred],env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=8)
            out=subprocess.run([ADB_BIN,'devices'],env=env,capture_output=True,text=True,timeout=5).stdout
            for line in out.splitlines()[1:]:
                parts=line.split()
                if len(parts)>=2 and parts[1]=='device' and parts[0]==preferred:
                    subprocess.run([ADB_BIN,'-s',preferred,'forward','tcp:9222','localabstract:chrome_devtools_remote'],env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=8)
                    return preferred
        except Exception:
            pass
    return ''

def device_screenshot_png():
    serial=device_serial()
    if not serial: raise RuntimeError('Android device ADB transport unavailable')
    proc=subprocess.run([ADB_BIN,'-s',serial,'exec-out','screencap','-p'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=8)
    if proc.returncode or not proc.stdout.startswith(b'\\x89PNG'):
        raise RuntimeError('Android screen capture unavailable: '+(proc.stderr.decode(errors='replace').strip() or 'no PNG returned'))
    return serial,proc.stdout

def get_json(path):
    with urllib.request.urlopen(CDP+path, timeout=5) as r:
        return json.loads(r.read().decode())

def target(preferred_id=None):
    pages=[x for x in get_json('/json/list') if x.get('type')=='page']
    if not pages:
        raise RuntimeError('No Chrome page target found')
    if preferred_id:
        for p in pages:
            if str(p.get('id','')) == str(preferred_id):
                return p
    def score(p):
        url=str(p.get('url','')).lower()
        title=str(p.get('title','')).lower()
        return (
            100 if TARGET_HINT and TARGET_HINT in url else 0,
            40 if 'ima' in title else 0,
            20 if 'imaosglobal.github.io' in url else 0
        )
    return sorted(pages,key=score,reverse=True)[0]

def cdp(method, params=None, preferred_id=None):
    t=target(preferred_id)
    ws=websocket.create_connection(t['webSocketDebuggerUrl'], timeout=8, suppress_origin=True)
    try:
        ws.send(json.dumps({'id':1,'method':method,'params':params or {}}))
        while True:
            msg=json.loads(ws.recv())
            if msg.get('id')==1:
                if 'error' in msg:
                    raise RuntimeError(msg['error'].get('message','CDP error'))
                return msg.get('result',{})
    finally:
        ws.close()

def evaluate(expression, preferred_id=None):
    return cdp('Runtime.evaluate', {'expression':expression,'returnByValue':True,'awaitPromise':True}, preferred_id)

def execute_action(action,payload):
    preferred_id=str(payload.get('target_id','')).strip() or None
    if action=='status':
        t=target(preferred_id)
        return {'ok':True,'target':{'id':t.get('id'),'title':t.get('title'),'url':t.get('url')}}
    if action=='tabs':
        return {'ok':True,'tabs':get_json('/json/list')}
    if action=='screenshot':
        return {'ok':True,'mime':'image/png','data':cdp('Page.captureScreenshot',{'format':'png','fromSurface':True}, preferred_id)['data']}
    if action=='device_screen':
        serial,raw=device_screenshot_png()
        return {'ok':True,'mime':'image/png','data':base64.b64encode(raw).decode('ascii'),'source':'android-device-screen','serial':serial}
    if action=='navigate':
        url=str(payload.get('url','')).strip()
        if not url.startswith(('https://','http://')):
            raise ValueError('url must be http(s)')
        evaluate('location.href='+json.dumps(url), preferred_id)
        return {'ok':True,'url':url}
    if action=='eval':
        if not LOCAL_EVAL_ENABLED:
            raise ValueError('local_eval_disabled')
        return {'ok':True,'result':evaluate(str(payload.get('expression',''))).get('result')}
    if action=='click':
        selector=str(payload.get('selector','')).strip()
        if not selector: raise ValueError('selector required')
        expr='(()=>{const e=document.querySelector('+json.dumps(selector)+');if(!e)return false;e.scrollIntoView({block:"center",inline:"center"});e.click();return true})()'
        ok=evaluate(expr, preferred_id).get('result',{}).get('value')
        return {'ok':bool(ok),'clicked':bool(ok)}
    if action=='tap':
        x=float(payload.get('x',0)); y=float(payload.get('y',0))
        cdp('Input.dispatchMouseEvent',{'type':'mouseMoved','x':x,'y':y}, preferred_id)
        cdp('Input.dispatchMouseEvent',{'type':'mousePressed','x':x,'y':y,'button':'left','clickCount':1}, preferred_id)
        cdp('Input.dispatchMouseEvent',{'type':'mouseReleased','x':x,'y':y,'button':'left','clickCount':1}, preferred_id)
        return {'ok':True,'x':x,'y':y}
    if action=='scroll':
        dx=float(payload.get('deltaX',0)); dy=float(payload.get('deltaY',0))
        cdp('Input.dispatchMouseEvent',{'type':'mouseWheel','x':float(payload.get('x',10)),'y':float(payload.get('y',10)),'deltaX':dx,'deltaY':dy}, preferred_id)
        return {'ok':True,'deltaX':dx,'deltaY':dy}
    if action=='type':
        return {'ok':True,'result':cdp('Input.insertText',{'text':str(payload.get('text',''))}, preferred_id)}
    if action=='key':
        key=str(payload.get('key','')).strip()
        if not key:
            raise ValueError('key required')
        keymap={
            'Enter':{'key':'Enter','code':'Enter','windowsVirtualKeyCode':13,'nativeVirtualKeyCode':13},
            'Escape':{'key':'Escape','code':'Escape','windowsVirtualKeyCode':27,'nativeVirtualKeyCode':27},
            'Tab':{'key':'Tab','code':'Tab','windowsVirtualKeyCode':9,'nativeVirtualKeyCode':9},
            'Backspace':{'key':'Backspace','code':'Backspace','windowsVirtualKeyCode':8,'nativeVirtualKeyCode':8},
            'ArrowLeft':{'key':'ArrowLeft','code':'ArrowLeft','windowsVirtualKeyCode':37,'nativeVirtualKeyCode':37},
            'ArrowRight':{'key':'ArrowRight','code':'ArrowRight','windowsVirtualKeyCode':39,'nativeVirtualKeyCode':39},
            'ArrowUp':{'key':'ArrowUp','code':'ArrowUp','windowsVirtualKeyCode':38,'nativeVirtualKeyCode':38},
            'ArrowDown':{'key':'ArrowDown','code':'ArrowDown','windowsVirtualKeyCode':40,'nativeVirtualKeyCode':40},
            'Space':{'key':' ','code':'Space','windowsVirtualKeyCode':32,'nativeVirtualKeyCode':32},
        }
        spec=keymap.get(key,{'key':key,'code':key})
        cdp('Input.dispatchKeyEvent',{'type':'keyDown',**spec}, preferred_id)
        cdp('Input.dispatchKeyEvent',{'type':'keyUp',**spec}, preferred_id)
        return {'ok':True,'key':key}
    raise ValueError('unsupported_action')

def cloud_request(path,method='GET',payload=None):
    body=None
    headers={'Accept':'application/json','User-Agent':'IMA-Termux-Bridge/1.0'}
    if DEVICE_KEY:
        headers['X-IMA-Device-Key']=DEVICE_KEY
    if payload is not None:
        body=json.dumps(payload).encode()
        headers['Content-Type']='application/json'
    req=urllib.request.Request(CLOUD_API+path,data=body,headers=headers,method=method)
    with urllib.request.urlopen(req,timeout=CLOUD_TIMEOUT) as r:
        raw=r.read()
        return r.status, json.loads(raw.decode()) if raw else {}

def upload_device_frame():
    if not DEVICE_KEY:
        return
    serial,raw=device_screenshot_png()
    req=urllib.request.Request(
        BROWSERGLASS_API+'/api/device/frame',
        data=raw,
        headers={
            'Content-Type':'image/png',
            'Cache-Control':'no-store',
            'X-IMA-Device-Key':DEVICE_KEY,
            'X-IMA-Device-Serial':serial,
        },
        method='POST',
    )
    with urllib.request.urlopen(req,timeout=CLOUD_TIMEOUT) as r:
        if r.status not in (200,201,202,204):
            raise RuntimeError('device frame relay HTTP '+str(r.status))

def device_frame_relay_loop():
    if not DEVICE_KEY:
        print('Device frame relay disabled: IMA_DEVICE_KEY is not configured.',flush=True)
        return
    delay=1.0
    while True:
        try:
            upload_device_frame()
            delay=1.0
            time.sleep(FRAME_UPLOAD_SECONDS)
        except Exception as e:
            print('Device frame relay:',str(e),flush=True)
            time.sleep(min(delay,30.0))
            delay=min(delay*2,30.0)

def persist_device_key(device_key, device_id=None):
    path=pathlib.Path(STATE_FILE)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps({'device_key':device_key,'device_id':device_id,'updated_at':time.time()},ensure_ascii=False),encoding='utf-8')
    try: path.chmod(0o600)
    except Exception: pass

def start_cloud_agent():
    global DEVICE_KEY
    if DEVICE_KEY and not any(t.name=='ima-cloud-agent' and t.is_alive() for t in threading.enumerate()):
        threading.Thread(target=cloud_agent_loop,daemon=True,name='ima-cloud-agent').start()
    if DEVICE_KEY and not any(t.name=='ima-device-frame-relay' and t.is_alive() for t in threading.enumerate()):
        threading.Thread(target=device_frame_relay_loop,daemon=True,name='ima-device-frame-relay').start()

CLOUD_ALLOWED_ACTIONS = frozenset({'status','tabs','screenshot','device_screen','navigate','click','tap','scroll','type','key'})

def execute_cloud_action(action, payload):
    # Cloud commands are authenticated device commands, but page/DOM content is untrusted.
    # Keep arbitrary JavaScript evaluation local-only so environmental text cannot turn
    # into a remote code-execution primitive through the device command plane.
    if action not in CLOUD_ALLOWED_ACTIONS:
        raise ValueError('cloud_action_not_allowed')
    return execute_action(action, payload)

def cloud_agent_loop():
    if not DEVICE_KEY:
        print('Cloud agent disabled: IMA_DEVICE_KEY is not configured.',flush=True)
        return
    delay=1.0
    while True:
        try:
            status, data=cloud_request('/ima-api/device/poll')
            if status==204 or not data.get('command'):
                delay=1.0
                time.sleep(CLOUD_POLL_SECONDS)
                continue
            cmd=data['command']
            result=execute_cloud_action(str(cmd.get('action')),cmd.get('payload') or {})
            cloud_request('/ima-api/device/result','POST',{'command_id':cmd.get('id'),'ok':True,'result':result})
            delay=1.0
        except Exception as e:
            try:
                if 'cmd' in locals() and cmd.get('id'):
                    cloud_request('/ima-api/device/result','POST',{'command_id':cmd.get('id'),'ok':False,'error':str(e)})
            except Exception:
                pass
            time.sleep(min(delay,30.0))
            delay=min(delay*2,30.0)

class ReusableHTTPServer(ThreadingHTTPServer):
    allow_reuse_address=True
    daemon_threads=True

class Handler(BaseHTTPRequestHandler):
    def send_json(self,obj,status=200):
        raw=json.dumps(obj,ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header('Content-Type','application/json; charset=utf-8')
        origin=self.headers.get('Origin','').rstrip('/')
        if origin and origin in ALLOWED_ORIGINS:
            self.send_header('Access-Control-Allow-Origin',origin)
            self.send_header('Vary','Origin')
        self.send_header('Access-Control-Allow-Headers','Content-Type, Authorization')
        self.send_header('Access-Control-Allow-Private-Network','true')
        self.send_header('Access-Control-Allow-Methods','GET,POST,OPTIONS')
        self.end_headers()
        self.wfile.write(raw)
    def do_OPTIONS(self):
        self.send_json({'ok':True})
    def do_GET(self):
        try:
            if self.path=='/status':
                t=target()
                self.send_json({'ok':True,'bridge':'ima-termux','port':PORT,'cdp':CDP,'cloud':{'enabled':bool(DEVICE_KEY),'api':CLOUD_API,'poll_seconds':CLOUD_POLL_SECONDS},'local_eval_enabled':LOCAL_EVAL_ENABLED,'target':{'id':t.get('id'),'title':t.get('title'),'url':t.get('url')}})
            elif self.path=='/tabs':
                self.send_json({'ok':True,'tabs':get_json('/json/list')})
            elif self.path=='/screenshot':
                self.send_json({'ok':True,'mime':'image/png','data':cdp('Page.captureScreenshot',{'format':'png','fromSurface':True})['data']})
            elif self.path=='/try-local-adb':
                local_ip=''
                try:
                    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM); s.connect(('8.8.8.8',80)); local_ip=s.getsockname()[0]; s.close()
                except Exception:
                    pass
                attempts=[]
                for port in (44867,46689,36369,5555):
                    if not local_ip: break
                    try:
                        p=subprocess.run([ADB_BIN,'connect',f'{local_ip}:{port}'],capture_output=True,text=True,timeout=5)
                        attempts.append({'target':f'{local_ip}:{port}','output':p.stdout.strip(),'error':p.stderr.strip()})
                    except Exception as exc:
                        attempts.append({'target':f'{local_ip}:{port}','error':str(exc)})
                serial=device_serial()
                self.send_json({'local_ip':local_ip,'attempts':attempts,'serial':serial})
            elif self.path=='/scan-adb':
                local_ip=''
                try:
                    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM); s.connect(('8.8.8.8',80)); local_ip=s.getsockname()[0]; s.close()
                except Exception:
                    pass
                found=[]
                if local_ip:
                    from concurrent.futures import ThreadPoolExecutor, as_completed
                    def probe(port):
                        try:
                            q=socket.create_connection((local_ip,port),timeout=0.08); q.close(); return port
                        except Exception: return None
                    with ThreadPoolExecutor(max_workers=200) as ex:
                        futures=[ex.submit(probe,p) for p in range(30000,50001)]
                        for fut in as_completed(futures):
                            p=fut.result()
                            if p is not None: found.append(p)
                            if len(found)>=20: break
                self.send_json({'local_ip':local_ip,'open_ports':sorted(found)})
            elif self.path=='/local-network-health':
                local_ip=''
                try:
                    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                    s.connect(('8.8.8.8',80))
                    local_ip=s.getsockname()[0]
                    s.close()
                except Exception as exc:
                    local_ip='error: '+str(exc)
                probes=[]
                for port in (36369,5555,5037):
                    ok=False
                    try:
                        q=socket.create_connection((local_ip,port),timeout=0.5)
                        q.close(); ok=True
                    except Exception:
                        pass
                    probes.append({'port':port,'open':ok})
                self.send_json({'local_ip':local_ip,'probes':probes})
            elif self.path=='/ui-dump':
                serial=device_serial()
                out=''
                if serial:
                    try:
                        p=subprocess.run([ADB_BIN,'-s',serial,'shell','uiautomator','dump','/dev/tty'],capture_output=True,text=True,timeout=12)
                        out=p.stdout.strip()
                    except Exception as exc: out='error: '+str(exc)
                self.send_json({'serial':serial,'ui':out})
            elif self.path=='/open-chrome-devtools-settings':
                serial=device_serial()
                result={}
                if serial:
                    env=dict(os.environ)
                    try:
                        p=subprocess.run([ADB_BIN,'-s',serial,'shell','am','start','-n','com.android.chrome/com.google.android.apps.chrome.Main','-d','chrome://settings/developerTools'],env=env,capture_output=True,text=True,timeout=10)
                        result['start']={'out':p.stdout.strip(),'err':p.stderr.strip(),'code':p.returncode}
                    except Exception as exc: result['start']={'error':str(exc)}
                self.send_json({'serial':serial,**result})
            elif self.path=='/refresh-chrome':
                serial=device_serial()
                result={}
                if serial:
                    env=dict(os.environ)
                    for label,args in [('stop',['shell','am','force-stop','com.android.chrome']),('start',['shell','monkey','-p','com.android.chrome','-c','android.intent.category.LAUNCHER','1'])]:
                        try:
                            p=subprocess.run([ADB_BIN,'-s',serial,*args],env=env,capture_output=True,text=True,timeout=10)
                            result[label]={'out':p.stdout.strip(),'err':p.stderr.strip(),'code':p.returncode}
                        except Exception as exc: result[label]={'error':str(exc)}
                    try:
                        p=subprocess.run([ADB_BIN,'-s',serial,'forward','tcp:9222','localabstract:chrome_devtools_remote'],env=env,capture_output=True,text=True,timeout=8)
                        result['forward']={'out':p.stdout.strip(),'err':p.stderr.strip(),'code':p.returncode}
                    except Exception as exc: result['forward']={'error':str(exc)}
                self.send_json({'serial':serial,**result})
            elif self.path=='/chrome-health':
                serial=device_serial()
                out={}
                if serial:
                    env=dict(os.environ)
                    for name,args in [('chrome_pid',['shell','pidof','com.android.chrome']),('devtools_socket',['shell','sh','-c','cat /proc/net/unix | grep -E "chrome_devtools_remote|webview_devtools_remote" | tail -20'])]:
                        try:
                            p=subprocess.run([ADB_BIN,'-s',serial,'*PLACEHOLDER*'] if False else [ADB_BIN,'-s',serial,*args],env=env,capture_output=True,text=True,timeout=8)
                            out[name]=p.stdout.strip(); out[name+'_error']=p.stderr.strip()
                        except Exception as exc: out[name+'_error']=str(exc)
                self.send_json({'serial':serial,**out})
            elif self.path=='/device-health':
                serial=device_serial()
                cdp_ok=False
                cdp_error=''
                mdns=''
                try:
                    pages=get_json('/json/list')
                    cdp_ok=bool([x for x in pages if x.get('type')=='page'])
                except Exception as exc:
                    cdp_error=str(exc)
                try:
                    env=dict(os.environ); env['ADB_MDNS_AUTO_CONNECT']='adb-tls-connect'
                    mdns=subprocess.run([ADB_BIN,'mdns','services'],env=env,capture_output=True,text=True,timeout=8).stdout
                except Exception as exc:
                    mdns='mdns_error: '+str(exc)
                self.send_json({'ok':bool(serial and cdp_ok),'serial':serial,'adb':bool(serial),'cdp':cdp_ok,'cdp_error':cdp_error,'mdns':mdns,'configured_serial':ADB_SERIAL,'port':PORT})
            elif self.path=='/device-screen':
                serial,raw=device_screenshot_png()
                self.send_response(200); self.send_header('Content-Type','image/png'); self.send_header('Cache-Control','no-store'); self.send_header('X-IMA-Device-Serial',serial); self.send_header('Content-Length',str(len(raw))); self.end_headers(); self.wfile.write(raw)
            else:
                self.send_json({'ok':False,'error':'not_found'},404)
        except Exception as e:
            self.send_json({'ok':False,'error':str(e)},503)
    def do_POST(self):
        try:
            origin=self.headers.get('Origin','').rstrip('/')
            path=urllib.parse.urlparse(self.path).path
            if path in ACTION_PATHS and origin and origin not in ALLOWED_ORIGINS:
                self.send_json({'ok':False,'error':'origin_not_allowed'},403)
                return
            if path in ACTION_PATHS and not origin:
                self.send_json({'ok':False,'error':'origin_required'},403)
                return
            n=int(self.headers.get('Content-Length','0'))
            body=json.loads(self.rfile.read(n) or b'{}')
            if path=='/enroll':
                auth=str(body.get('authorization','')).strip()
                if not auth.startswith('Bearer '):
                    raise ValueError('authorization required')
                req=urllib.request.Request(CLOUD_API+'/ima-api/device/register',data=json.dumps({'device_label':'Android Chrome · Termux','platform':'android-termux','capabilities':{'browser':True,'chrome_cdp':True,'network_independent':True,'internet_screen_relay':True},'metadata':{'bridge':'ima-termux-bridge','target_hint':TARGET_HINT}}).encode(),headers={'Content-Type':'application/json','Authorization':auth,'Accept':'application/json'},method='POST')
                with urllib.request.urlopen(req,timeout=CLOUD_TIMEOUT) as rr:
                    data=json.loads(rr.read().decode())
                if not data.get('device_key'): raise RuntimeError('cloud enrollment returned no device key')
                DEVICE_KEY=str(data['device_key']).strip()
                persist_device_key(DEVICE_KEY,(data.get('device') or {}).get('id'))
                start_cloud_agent()
                self.send_json({'ok':True,'enrolled':True,'device':data.get('device'), 'cloud':{'api':CLOUD_API,'network_independent':True}})
            elif path in ('/navigate','/eval','/click','/tap','/scroll','/type','/key'):
                action=path[1:]
                self.send_json(execute_action(action,body))
            else:
                self.send_json({'ok':False,'error':'not_found'},404)
        except Exception as e:
            self.send_json({'ok':False,'error':str(e)},503)

if __name__=='__main__':
    if DEVICE_KEY:
        start_cloud_agent()
    print('IMA bridge listening on http://127.0.0.1:'+str(PORT),flush=True)
    print('IMA full Android screen channel: /device-screen, cloud relay and action=device_screen',flush=True)
    print('Chrome CDP: '+CDP,flush=True)
    print('Chrome target hint: '+TARGET_HINT,flush=True)
    ReusableHTTPServer((HOST,PORT),Handler).serve_forever()
