#!/data/data/com.termux/files/usr/bin/python
import json, re, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import bridge
from mcp_client import IMA_MCPClient

mcp=IMA_MCPClient()

def _json_body(handler):
    n=int(handler.headers.get("Content-Length","0"))
    return json.loads(handler.rfile.read(n) or b"{}")

def _send(handler,obj,status=200):
    handler.send_json(obj,status)

def _context():
    return mcp.context_package()

def _live001_status():
    tools=mcp.tools_list()
    live=next((t for t in tools if t.get("name")=="ima_live_browser"),None)
    return {"ok":bool(live),"canonical":True,"id":"LIVE-001","tool":"ima_live_browser","available":bool(live),"protocol":mcp.protocol_version,"session_established":bool(mcp.session_id)}

def _parse_call(text):
    match=re.search(r'IMA_CALL\s*:\s*(\{.*?\})',text or "",re.S)
    if not match:
        return None
    try:
        obj=json.loads(match.group(1))
    except json.JSONDecodeError:
        return None
    if not isinstance(obj,dict) or not obj.get("tool"):
        return None
    return {"tool":obj["tool"],"args":obj.get("args") or obj.get("arguments") or {}}

_original_get=bridge.Handler.do_GET
_original_post=bridge.Handler.do_POST

def do_GET(self):
    path=self.path.split("?",1)[0]
    if path=="/mcp/status":
        try:
            return _send(self,{"ok":True,"mcp":_context()})
        except Exception as e:
            return _send(self,{"ok":False,"error":str(e)},503)
    if path=="/live001/status":
        try:
            return _send(self,_live001_status())
        except Exception as e:
            return _send(self,{"ok":False,"canonical":True,"id":"LIVE-001","error":str(e)},503)
    if path=="/mcp/tools":
        try:
            return _send(self,{"ok":True,"tools":mcp.tools_list(),"protocol":mcp.protocol_version,"session":bool(mcp.session_id)})
        except Exception as e:
            return _send(self,{"ok":False,"error":str(e)},503)
    return _original_get(self)

def do_POST(self):
    path=self.path.split("?",1)[0]
    if path=="/mcp/call":
        try:
            body=_json_body(self)
            name=str(body.get("tool","")).strip()
            if not name:
                raise ValueError("tool required")
            result=mcp.tools_call(name,body.get("args") or body.get("arguments") or {})
            return _send(self,{"ok":True,"tool":name,"result":result,"protocol":mcp.protocol_version})
        except Exception as e:
            return _send(self,{"ok":False,"error":str(e)},503)
    if path=="/mcp/context":
        try:
            return _send(self,{"ok":True,"context":_context()})
        except Exception as e:
            return _send(self,{"ok":False,"error":str(e)},503)
    if path=="/mcp/parse":
        try:
            body=_json_body(self)
            call=_parse_call(str(body.get("text","")))
            if not call:
                return _send(self,{"ok":False,"error":"IMA_CALL not found"},400)
            result=mcp.tools_call(call["tool"],call["args"])
            return _send(self,{"ok":True,"parsed":call,"result":result})
        except Exception as e:
            return _send(self,{"ok":False,"error":str(e)},503)
    return _original_post(self)

bridge.Handler.do_GET=do_GET
bridge.Handler.do_POST=do_POST

if __name__=="__main__":
    if bridge.DEVICE_KEY:
        bridge.start_cloud_agent()
    print("IMA canonical bridge + MCP relay listening on http://127.0.0.1:"+str(bridge.PORT),flush=True)
    print("MCP endpoints: /mcp/status /mcp/tools /mcp/context /mcp/call /mcp/parse",flush=True)
    bridge.ReusableHTTPServer((bridge.HOST,bridge.PORT),bridge.Handler).serve_forever()
