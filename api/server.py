
#!/usr/bin/env python3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
print("PYTHON ROOT:", ROOT, flush=True)

from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import json,time,requests
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

# Canonical provider-neutral intelligence gateway. It preserves IMA identity while
# allowing authorized present/future intelligences to answer through one boundary.
try:
    from importlib.util import spec_from_file_location, module_from_spec
    _uig_spec = spec_from_file_location(
        "ima_universal_intelligence_gateway",
        str(ROOT / ".ima" / "intelligence" / "universal_intelligence_gateway.py")
    )
    _uig_module = module_from_spec(_uig_spec)
    _uig_spec.loader.exec_module(_uig_module)
    universal_intelligence_route = _uig_module.route
except Exception:
    universal_intelligence_route = None

# Co-Cognition: shared human/IMA reasoning layer.
try:
    from .ima_co_cognition_import import load_co_cognition
except Exception:
    load_co_cognition = None

try:
    from importlib.util import spec_from_file_location, module_from_spec
    _cc_spec = spec_from_file_location(
        "ima_co_cognition",
        str(ROOT / ".ima" / "co_cognition" / "engine.py")
    )
    _cc_module = module_from_spec(_cc_spec)
    _cc_spec.loader.exec_module(_cc_module)
    co_cognition = _cc_module
except Exception:
    co_cognition = None
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
        context = conversation_layer.context(self.user_id())

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
                "response":"שלום. אני אמא — של כולם. השיחה והזיכרון האישי שלך נשמרים במרחב שלך; הידע הציבורי של אמא נבנה ממקורות רבים." 
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



def create_live_browser_session(user_id):
    if not user_id or user_id == "anonymous":
        return {"error":"authentication_required","status":"ERROR"}
    api_key=os.environ.get("FIRECRAWL_API_KEY")
    if not api_key:
        return {"error":"live_browser_not_configured","status":"ERROR"}
    response=requests.post(
        "https://api.firecrawl.dev/v1/interact",
        headers={"Authorization":f"Bearer {api_key}","Content-Type":"application/json"},
        json={"url":"https://imaosglobal.github.io/Ima-kernel/","prompt":"Open the IMA public site and keep a live browser session available for the authenticated IMA user. Do not sign in or submit forms automatically."},
        timeout=45,
    )
    if response.status_code >= 400:
        return {"error":"live_browser_provider_error","provider_status":response.status_code,"status":"ERROR"}
    data=response.json()
    result=data.get("result") if isinstance(data,dict) else None
    if isinstance(result,dict):
        for key in ("interactiveLiveViewUrl","liveViewUrl","sessionUrl"):
            if result.get(key):
                return {key:result[key],"scrapeId":data.get("scrapeId"),"status":"OK"}
    for key in ("interactiveLiveViewUrl","liveViewUrl","sessionUrl"):
        if isinstance(data,dict) and data.get(key):
            return {key:data[key],"scrapeId":data.get("scrapeId"),"status":"OK"}
    return {"error":"live_browser_url_missing","status":"ERROR"}


BRAIN=Brain()


class Handler(BaseHTTPRequestHandler):

    def user_id(self):
        return self.headers.get('X-IMA-User') or 'anonymous'

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

        elif self.path=="/intelligence/status":
            if universal_intelligence_route is not None:
                try:
                    module = _uig_module
                    self.send_json(module.status())
                except Exception as e:
                    self.send_json({"gateway":"ERROR","error":str(e)})
            else:
                self.send_json({"gateway":"UNAVAILABLE"})

        else:
            self.send_json({
                "product":"IMA",
                "status":"ONLINE"
            })


    def do_POST(self):
        try:
            if self.path == "/browser/session":
                result=create_live_browser_session(self.user_id())
                self.send_json(result)
                return

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
                    # Use the same provider-neutral IMA gateway on the public site.
                    # It selects only already-authorized providers; it never invents
                    # a connection and never broadens private data scope implicitly.
                    gateway_answer = None
                    if universal_intelligence_route is not None:
                        try:
                            gateway_answer = universal_intelligence_route(
                                question,
                                private=True,
                                high_impact=False,
                            )
                        except Exception as gateway_error:
                            print("UNIVERSAL INTELLIGENCE GATEWAY:", gateway_error, flush=True)

                    if gateway_answer and gateway_answer.get("status") == "OK" and gateway_answer.get("response"):
                        answer = {
                            "response": gateway_answer["response"],
                            "status": "OK",
                            "intelligence_gateway": gateway_answer.get("gateway"),
                            "provider": gateway_answer.get("provider"),
                            "truth_state": gateway_answer.get("truth_state"),
                            "verification_required": gateway_answer.get("verification_required", True),
                        }
                    else:
                        try:
                            answer = ima_master_runtime.ask(question, user_id=self.user_id(), public=True)

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

                # Co-Cognition happens after the response exists:
                # human contribution + IMA contribution -> shared insight.
                try:
                    if co_cognition is not None:
                        cc_context = conversation_layer.context()
                        cc_result = co_cognition.analyze(
                            question,
                            context=cc_context,
                            ima_response=(
                                answer.get("response", "")
                                if isinstance(answer, dict)
                                else str(answer)
                            ),
                        )
                        co_cognition.record(cc_result)
                except Exception as e:
                    print("CO-COGNITION:", e, flush=True)

                conversation_layer.update(
                    question,
                    (
                        answer.get("response", "")
                        if isinstance(answer, dict)
                        else str(answer)
                    )
                , self.user_id())

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
