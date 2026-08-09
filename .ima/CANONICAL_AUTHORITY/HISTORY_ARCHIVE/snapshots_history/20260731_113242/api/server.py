#!/usr/bin/env python3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
print("PYTHON ROOT:", ROOT, flush=True)

from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import json,time
from core.conversation_router import route
print('BOOT: before ima_master_runtime', flush=True)
import ima_master_runtime
print('BOOT: after ima_master_runtime', flush=True)
import sys
from pathlib import Path


print("PYTHON ROOT:", ROOT, flush=True)
import os
sys.path.append('..')
import identity_context
print('BOOT: before conversation_layer', flush=True)
import conversation_layer
print('BOOT: after conversation_layer', flush=True)
print('BOOT: before product_gateway', flush=True)
from product.gateway import product_gateway
print('BOOT: after product_gateway', flush=True)



def supabase_status():
    try:
        from api.database.supabase_env import load_env
        load_env()

        from api.database.supabase_rest import supabase_get

        result=supabase_get("users")

        return {
            "provider":"supabase",
            "connected": result.get("status")==200
        }

    except Exception as e:
        return {
            "provider":"supabase",
            "connected":False,
            "error":str(e)
        }


from api.database.memory_store import load_memory, save_memory

class Brain:

    def __init__(self):
        try:
            self.memory = [
                x.get("content","")
                for x in load_memory()
            ]
        except:
            self.memory=[]


    def process(self, question):

        q=question.strip()
        context = conversation_layer.context()

        try:
            from api.database.memory_store import load_memory
            memories = load_memory()
            context["supabase_memory"] = [
                x.get("content","")
                for x in memories[-10:]
            ]
        except Exception:
            context["supabase_memory"] = []

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
            save_memory(q)
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

        memories = context.get("supabase_memory", [])

        return {
            "response":
            "אני כאן. קיבלתי: " + q +
            "\n\nזיכרון Supabase אחרון:\n" +
            "\n".join(memories[-5:])
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


    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-Type","application/json")
        self.end_headers()

    def do_GET(self):

        if self.path=="/health":
            self.send_json({
                "health":"ok",
                "brain":True
            })

        elif self.path=="/ready":
            self.send_json({
                "ready":True,
                "runtime":True,
                "memory":True,
                "conversation":True,
                "gateway":True,
                "brain":True
            })

        elif self.path=="/supabase/status":
            self.send_json(supabase_status())

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

                clean = None

                try:
                    clean = route(question)
                except Exception:
                    clean = None

                if clean:
                    answer = {
                        "response": clean,
                        "status": "OK"
                    }
                else:
                    try:
                        answer = ima_master_runtime.ask(question)

                        if isinstance(answer, dict):
                            response = answer.get("response","")

                            if (
                                not response
                                or "אין זיכרון" in response
                                or "עדיין אין" in response
                            ):
                                from api.database.memory_store import load_memory

                                memories = load_memory()

                                if memories:
                                    answer["response"] = "\n\n".join(
                                        x.get("content","")
                                        for x in memories[-20:]
                                        if x.get("content")
                                        and x.get("content","").strip() != question.strip()
                                        and len(x.get("content","").strip()) > len(question.strip())
                                    )

                    except Exception:
                        answer = product_gateway.ask(question)

                conversation_layer.update(question)

                try:
                    from api.database.memory_store import save_memory
                    save_memory(
                        question + "\n" +
                        (answer.get("response","") if isinstance(answer, dict) else str(answer))
                    )
                except Exception:
                    pass

                try:
                    if isinstance(answer, dict):
                        if answer.get("response") in [
                            "עדיין אין לי מספיק זיכרון שיחה למצוא.",
                            "אין זיכרון מתאים נמצא ב-Supabase או בזיכרון המקומי."
                        ]:
                            memories = load_memory()
                            if memories:
                                answer["response"] = "\n".join(
                                    x.get("content","")
                                    for x in memories[-5:]
                                    if x.get("content","")
                                )
                            else:
                                answer["response"] = "אין זיכרון שמור עדיין."
                except Exception:
                    pass

                self.send_json({
                    "input": question,
                    "answer": answer,
                    "time": int(time.time()),
                    "status": "OK"
                })

            else:
                self.send_json({
                    "error":"unknown endpoint",
                    "path":self.path
                })

        except Exception as e:
            self.send_json({
                "status":"ERROR",
                "error":str(e)
            })

PORT=int(os.environ.get("PORT",8080))
print(f"IMA API ONLINE :{PORT}", flush=True)
HTTPServer(("0.0.0.0",PORT),Handler).serve_forever()
