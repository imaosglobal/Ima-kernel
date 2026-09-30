import time
import identity_context
import conversation_layer
import ima_brain
from learning.learning_loop import learn_from_event
import ima_mom
from learning.knowledge_answer_builder import build_answer
from learning.knowledge_graph_retrieval import search_concept

try:
    from connectors.llm.router import ask_models
except Exception:
    ask_models = None

try:
    from connectors.llm.ima_pipeline import ask as ima_llm_answer
except Exception:
    ima_llm_answer = None

try:
    import ima_system
    SYSTEM = True
except Exception:
    SYSTEM = False

class IMAMaster:
    def __init__(self):
        self.name = "IMA MASTER"

    def ask(self, message, user_id="default", public=False, public_memory=None):
        context = identity_context.build_context(message, public=public)
        result = {
            "time": time.time(),
            "identity": context.get("identity", {}),
            "laws": context.get("laws", []),
            "vision": context.get("vision", {}),
            "message": message,
            "connections": {
                "identity": True, "memory": True, "brain": True, "mother": True,
                "system": SYSTEM, "public_mode": public,
                "user_scope": "per-user" if public else user_id,
            }
        }

        if "מי אני" in message:
            result["response"] = context.get("legacy", "")
        elif "חוקים" in message:
            result["response"] = "\n".join(context.get("laws", []))
        elif "מטרה" in message or "חזון" in message:
            result["response"] = context.get("vision", {}).get("goal", "") + "\n\n" + context.get("vision", {}).get("belief", "")
        else:
            try:
                events = [] if public else ima_brain.load_events()
                if ask_models is not None:
                    try:
                        result["llm"] = ask_models(message)
                    except Exception as exc:
                        result["llm"] = {"status": "error", "error": str(exc)}

                llm_answer = None
                if ima_llm_answer is not None:
                    try:
                        candidate = ima_llm_answer(message)
                        if isinstance(candidate, dict):
                            status = candidate.get("status")
                            text = candidate.get("response") or candidate.get("text")
                            if status not in ("no_provider", "error") and text:
                                llm_answer = str(text)
                                result["llm_response"] = candidate
                            elif status == "error":
                                result["llm_error"] = candidate.get("error") or candidate.get("attempted")
                        elif isinstance(candidate, str) and candidate.strip():
                            llm_answer = candidate.strip()
                    except Exception as exc:
                        result["llm_error"] = str(exc)

                if llm_answer:
                    result["response"] = llm_answer
                else:
                    brain_answer = None
                    try:
                        nodes = search_concept(message)
                        if nodes:
                            brain_answer = build_answer({"domain": "knowledge_graph", "content": nodes}, message)
                    except Exception as exc:
                        result["knowledge_error"] = str(exc)
                    if not brain_answer and not public:
                        brain_answer = ima_brain.answer(message, events)
                    if brain_answer:
                        result["response"] = brain_answer
                    elif public_memory:
                        result["response"] = "מצאתי הקשר בזיכרון הפרטי של השיחה שלך:\n" + "\n".join(x.get("response", "") for x in public_memory[-5:])
                    else:
                        result["response"] = ima_mom.generate_answer(message, ima_mom.load())
            except Exception as exc:
                result["response"] = "IMA runtime fallback: " + str(exc)

        if not public:
            conversation_layer.update(message, result.get("response", ""))
            try:
                if len(message.strip()) > 8:
                    learn_from_event({"source": "user", "user_id": user_id, "text": message, "response": result.get("response", "")})
            except Exception:
                pass
        return result

IMA = IMAMaster()

def ask(message, user_id="default", public=False, public_memory=None):
    return IMA.ask(message, user_id=user_id, public=public, public_memory=public_memory)
