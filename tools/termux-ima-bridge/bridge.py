#!/usr/bin/env python3
import base64, json, os, sys, time, threading, urllib.request, urllib.parse, pathlib, subprocess, socket, uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from queue import Queue, Empty

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
DOWNLOADS=pathlib.Path(os.path.expanduser(os.environ.get('IMA_ANDROID_DOWNLOADS','~/storage/downloads')))
NATIVE_ANDROID_ACTIONS={'android_screenshot':'screenshot','android_navigate':'navigate','android_tap':'tap','android_swipe':'swipe','android_text':'text','android_key':'key','android_back':'back','android_home':'home','android_read_text':'read_text','android_status':'status'}
NATIVE_LOCK=threading.Lock()
NATIVE_COMMANDS=Queue()
NATIVE_RESULTS={}
NATIVE_PROVIDER={'online':False,'package':'','version':'','last_seen':0.0}
NATIVE_PROVIDER_LOCK=threading.Lock()

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

def native_android_command(action,payload=None,timeout=25):
    native=NATIVE_ANDROID_ACTIONS.get(action)
    if not native:
        raise ValueError('unsupported_native_android_action')
    with NATIVE_LOCK:
        return _native_android_command_locked(action,payload,timeout)

def _native_android_command_locked(action,payload=None,timeout=25):
    native=NATIVE_ANDROID_ACTIONS.get(action)
    if not native:
        raise ValueError('unsupported_native_android_action')
    with NATIVE_PROVIDER_LOCK:
        online=bool(NATIVE_PROVIDER.get('online'))
        last=float(NATIVE_PROVIDER.get('last_seen') or 0)
    if not online or time.time()-last>8:
        raise RuntimeError('native Android transport unavailable: Accessibility provider is offline')
    command_id=str(uuid.uuid4())
    NATIVE_COMMANDS.put({'id':command_id,'action':native,**(payload or {})})
    deadline=time.time()+timeout
    while time.time()<deadline:
        with NATIVE_PROVIDER_LOCK:
            result=NATIVE_RESULTS.pop(command_id,None)
        if result is not None:
            if not result.get('ok'):
                raise RuntimeError(result.get('error') or result.get('message') or 'native_android_action_failed')
            return result
        time.sleep(0.1)
    raise TimeoutError('native Android transport timed out; accessibility service is not online')
