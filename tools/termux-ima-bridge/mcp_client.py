#!/usr/bin/env python3
"""Minimal provider-neutral MCP Streamable HTTP client for the canonical IMA bridge."""
import json, os, uuid, urllib.request, urllib.error

MCP_URL=os.environ.get("IMA_MCP_URL","https://ima-universal-action-core.onrender.com/mcp").rstrip("/")
MCP_PROTOCOL=os.environ.get("IMA_MCP_PROTOCOL_VERSION","2025-06-18")

class MCPError(RuntimeError): pass

class IMA_MCPClient:
    def __init__(self,url=MCP_URL):
        self.url=url.rstrip("/")
        self.session_id=None
        self.protocol_version=MCP_PROTOCOL
        self.server_info={}
        self.capabilities={}

    def _post(self,payload,include_session=True):
        headers={"Content-Type":"application/json","Accept":"application/json, text/event-stream"}
        if include_session and self.session_id:
            headers["Mcp-Session-Id"]=self.session_id
        req=urllib.request.Request(self.url,data=json.dumps(payload).encode(),headers=headers,method="POST")
        try:
            with urllib.request.urlopen(req,timeout=20) as r:
                raw=r.read().decode("utf-8","replace")
                sid=r.headers.get("Mcp-Session-Id") or r.headers.get("mcp-session-id")
                if sid: self.session_id=sid
                return r.status,raw
        except urllib.error.HTTPError as e:
            raise MCPError(f"MCP HTTP {e.code}: {e.read().decode('utf-8','replace')[:1000]}")

    @staticmethod
    def _parse(raw):
        raw=raw.strip()
        if not raw: return {}
        try: return json.loads(raw)
        except json.JSONDecodeError:
            data=[x[5:] for x in raw.splitlines() if x.startswith("data:")]
            if data:
                try: return json.loads("\n".join(data))
                except json.JSONDecodeError: pass
        raise MCPError("MCP response was not JSON/JSON-SSE")

    def initialize(self):
        status,raw=self._post({
            "jsonrpc":"2.0","id":str(uuid.uuid4()),"method":"initialize",
            "params":{"protocolVersion":self.protocol_version,"capabilities":{},
                      "clientInfo":{"name":"ima-termux-bridge","version":"1.0.0"}}
        },False)
        if status<200 or status>=300: raise MCPError(f"initialize HTTP {status}")
        msg=self._parse(raw)
        if "error" in msg: raise MCPError(json.dumps(msg["error"],ensure_ascii=False))
        result=msg.get("result") or {}
        self.protocol_version=result.get("protocolVersion",self.protocol_version)
        self.server_info=result.get("serverInfo") or {}
        self.capabilities=result.get("capabilities") or {}
        self._post({"jsonrpc":"2.0","method":"notifications/initialized","params":{}})
        return result

    def tools_list(self):
        if not self.session_id: self.initialize()
        status,raw=self._post({"jsonrpc":"2.0","id":str(uuid.uuid4()),"method":"tools/list","params":{}})
        msg=self._parse(raw)
        if "error" in msg: raise MCPError(json.dumps(msg["error"],ensure_ascii=False))
        return (msg.get("result") or {}).get("tools") or []

    def tools_call(self,name,args=None):
        if not self.session_id: self.initialize()
        status,raw=self._post({"jsonrpc":"2.0","id":str(uuid.uuid4()),"method":"tools/call",
                               "params":{"name":name,"arguments":args or {}}})
        msg=self._parse(raw)
        if "error" in msg: raise MCPError(json.dumps(msg["error"],ensure_ascii=False))
        return msg.get("result") or {}

    def context_package(self):
        tools=self.tools_list()
        return {
            "source":"IMA MCP",
            "endpoint":self.url,
            "protocol":self.protocol_version,
            "session_established":bool(self.session_id),
            "server":self.server_info,
            "capabilities":self.capabilities,
            "tools":[{"name":t.get("name"),"description":t.get("description",""),"inputSchema":t.get("inputSchema",{})} for t in tools],
        }
