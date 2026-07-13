#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import json,time
import ima_master_runtime
import sys
sys.path.append('..')
import identity_context
import conversation_layer
from product.gateway import product_gateway

MEMORY_FILE=Path("ima_memory.json")

class Brain:

    def __init__(self):
        if MEMORY_FILE.exists():
            try:
                self.memory=json.loads(
                    MEMORY_FILE.read_text(encoding="utf-8")
                )
            except:
                self.memory=[]
        else:
            self.memory=[]


    def process(self, question):

        q=question.strip()
        context = conversation_layer.context()

        if any(x in q for x in ["שלום","היי","הי","בוקר","ערב"]):
            return {
                "response":"שלום אורי. אני כאן. איך אפשר לעזור?"
            }

        if any(x in q for x in ["מי זאת","מי את","מי אתה","מה זה IMA"]):
            identity=Path("IMA_IDENTITY.md").read_text(encoding="utf-8")
            return {
                "response":"אני IMA.\n\n"+identity[:3000]
            }

        if any(x in q for x in ["תשמרי","תזכרי","זכור"]):
            self.memory.append(q)
            MEMORY_FILE.write_text(
                json.dumps(self.memory,ensure_ascii=False,indent=2),
                encoding="utf-8"
            )
            return {
                "response":"שמרתי בזיכרון המקומי: "+q
            }

        if "מי אני" in q:
            user=context.get("user", {})
            history=context.get("history", [])

            return {
                "response":
                "המשתמש שלי: " + str(user) +
                "\n\nהיסטוריית שיחה אחרונה:\n" +
                "\n".join(
                    x.get("message","") for x in history
                )
            }

        return {
            "response":"אני כאן. קיבלתי: "+q
        }


BRAIN=Brain()


class Handler(BaseHTTPRequestHandler):

    def send_json(self,data):
        body=json.dumps(data,ensure_ascii=False).encode()
        self.send_response(200)
        self.send_header("Content-Type","application/json")
        self.send_header("Access-Control-Allow-Origin","*")
        self.end_headers()
        self.wfile.write(body)


    def do_GET(self):

        if self.path=="/health":
            self.send_json({
                "health":"ok",
                "brain":True
            })
        else:
            self.send_json({
                "product":"IMA",
                "status":"ONLINE"
            })


    def do_POST(self):

        try:
            if self.path == "/ask":

                size = int(self.headers.get("Content-Length",0))
                raw = self.rfile.read(size)

                data = json.loads(raw)

                question = data.get("message") or data.get("question","")

                answer = product_gateway.ask(question)

                conversation_layer.update(question)

                self.send_json({
                    "input": question,
                    "answer": answer,
                    "time": int(time.time()),
                    "status": "OK"
                })

            else:
                self.send_json({
                    "error": "unknown endpoint",
                    "path": self.path
                })

        except Exception as e:

            self.send_json({
                "status": "ERROR",
                "error": str(e)
            })


print("IMA API ONLINE :8080")
HTTPServer(("0.0.0.0",8080),Handler).serve_forever()
