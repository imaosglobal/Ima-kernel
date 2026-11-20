#!/data/data/com.termux/files/usr/bin/python
import os,time,subprocess,urllib.request,pathlib
URL=os.environ.get("IMA_DEVICE_FRAME_URL","https://ima-browserglass.onrender.com/api/device/frame")
KEY=pathlib.Path("/data/data/com.termux/files/home/Ima-kernel/.ima/device-frame-key").read_text().strip()
ADB="/data/data/com.termux/files/usr/bin/adb"; LOG="/data/data/com.termux/files/home/.ima_bridge/frame-publisher.log"
def log(s):
    with open(LOG,"a",encoding="utf-8") as f: f.write(time.strftime("%H:%M:%S")+" "+s+"\n")
def serial():
    out=subprocess.run([ADB,"devices"],capture_output=True,text=True,timeout=5).stdout
    for line in out.splitlines()[1:]:
        p=line.split()
        if len(p)>=2 and p[1]=="device": return p[0]
    return ""
last=""
while True:
    try:
        s=serial()
        if s:
            p=subprocess.run([ADB,"-s",s,"exec-out","screencap","-p"],capture_output=True,timeout=8)
            raw=p.stdout
            if p.returncode==0 and raw.startswith(b"\x89PNG"):
                req=urllib.request.Request(URL,data=raw,method="POST",headers={"Content-Type":"image/png","X-IMA-Device-Key":KEY,"X-IMA-Device-Serial":s})
                try:
                    with urllib.request.urlopen(req,timeout=6) as r:
                        code=r.status; origin=r.headers.get("x-render-origin-server","")
                    state="post:"+str(code)+":"+origin
                    if state!=last: log(state)
                    last=state
                except Exception as e:
                    state="post-error"
                    if state!=last: log(state+" "+repr(e))
                    last=state
            else:
                if last!="capture-error": log("capture-error")
                last="capture-error"
        else:
            if last!="no-device": log("no-device")
            last="no-device"
    except Exception as e:
        if last!="loop-error": log("loop-error "+repr(e))
        last="loop-error"
    time.sleep(0.25)
