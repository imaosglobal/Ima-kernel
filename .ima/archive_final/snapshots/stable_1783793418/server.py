#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import json,time,sys
from pathlib import Path

sys.path.insert(0,".")

try:
    from learning import meta_orchestrator
    class Brain:
        def process(self, question):
            if "מי זאת" in question or "IMA" in question:
                identity = Path("IMA_IDENTITY.md").read_text(encoding="utf-8")
                return {
                    "identity": "IMA",
                    "identity_source": "IMA_IDENTITY.md",
                    "identity_document": identity[:3000],
                    "document": identity[:2000],
                    "meta": meta_orchestrator.run_meta_analysis()
                }
            return meta_orchestrator.run_meta_analysis()

        def run_meta_analysis(self):
            return meta_orchestrator.run_meta_analysis()

    BRAIN=Brain()
except Exception as e:
    BRAIN=None
    ERROR=str(e)


class Handler(BaseHTTPRequestHandler):

    def send_json(self,data):
        body=json.dumps(data,ensure_ascii=False).encode()
        self.send_response(200)
        self.send_header("Content-Type","application/json")
        self.end_headers()
        self.wfile.write(body)


    def do_GET(self):

        if self.path=="/":
            self.send_json({
                "product":"IMA",
                "status":"ONLINE",
                "runtime":"canonical",
                "brain":BRAIN is not None
            })

        elif self.path=="/health":
            self.send_json({
                "health":"ok",
                "brain":BRAIN is not None
            })

        else:
            self.send_json({"error":"not_found"})


    def do_POST(self):

        if self.path=="/ask":

            size=int(self.headers.get("Content-Length",0))
            data=json.loads(self.rfile.read(size))

            question=data.get("message","")

            if BRAIN:
                try:
                    answer=BRAIN.process(question)
                except Exception as e:
                    answer={"error":str(e)}
            else:
                answer={"error":"brain_offline"}

            self.send_json({
                "input":question,
                "answer":answer,
                "time":int(time.time())
            })

        else:
            self.send_json({"error":"not_found"})


print("IMA API ONLINE :8080")
HTTPServer(("0.0.0.0",8080),Handler).serve_forever()
