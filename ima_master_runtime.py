import time
import identity_context
import conversation_layer
import ima_brain
from learning.learning_loop import learn_from_event
import ima_mom
from learning.knowledge_answer_builder import build_answer
from learning.knowledge_expansion_engine import expand_knowledge
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
    from connectors.llm.auto_runtime import run as auto_llm_run
except Exception:
    auto_llm_run = None

try:
    import ima_system
    SYSTEM=True
except:
    SYSTEM=False

class IMAMaster:

    def __init__(self):
        self.name="IMA MASTER"

    def ask(self,message):

        context=identity_context.build_context(message)

        result={
            "time":time.time(),
            "identity":context.get("identity",{}),
            "laws":context.get("laws",[]),
            "vision":context.get("vision",{}),
            "message":message,
            "connections":{
                "identity":True,
                "memory":True,
                "brain":True,
                "mother":True,
                "system":SYSTEM
            }
        }

        if "מי אני" in message:
            result["response"]=context.get("legacy","")

        elif "חוקים" in message:
            result["response"]="\n".join(context.get("laws",[]))

        elif "מטרה" in message or "חזון" in message:
            result["response"]=(
                context.get("vision",{}).get("goal","")
                + "\n\n" +
                context.get("vision",{}).get("belief","")
            )

        else:
            try:
                events = ima_brain.load_events()

                # Expose the real connector state without claiming external
                # providers are connected when credentials are absent.
                if ask_models is not None:
                    try:
                        result["llm"] = ask_models(message)
                    except Exception as e:
                        result["llm"] = {"status": "error", "error": str(e)}

                # Use a configured LLM provider as the answer layer when one
                # is actually available. Otherwise continue through IMA's
                # local system/brain/memory layers.
                llm_answer = None
                if ima_llm_answer is not None:
                    try:
                        candidate = ima_llm_answer(message)
                        if isinstance(candidate, dict):
                            status = candidate.get("status")
                            candidate_text = candidate.get("response") or candidate.get("text")
                            if status not in ("no_provider", "error") and candidate_text:
                                llm_answer = str(candidate_text)
                                result["llm_response"] = candidate
                            elif status == "error":
                                result["llm_error"] = candidate.get("error") or candidate.get("attempted")
                                result["llm_response"] = candidate
                        elif isinstance(candidate, str) and candidate.strip():
                            llm_answer = candidate.strip()
                    except Exception as e:
                        result["llm_error"] = str(e)

                if llm_answer:
                    result["response"] = llm_answer
                    brain_answer = None
                else:
                    brain_answer = None
                    try:
                        knowledge_nodes = search_concept(message)
                        if knowledge_nodes:
                            brain_answer = build_answer(
                                {
                                    "domain": "knowledge_graph",
                                    "content": knowledge_nodes,
                                },
                                message,
                            )
                    except Exception as e:
                        result["knowledge_error"] = str(e)

                    if not brain_answer:
                        brain_answer = ima_brain.answer(
                            message,
                            events
                        )

                if brain_answer:
                    result["response"] = brain_answer
                else:
                    memory_hits = conversation_layer.recall(message)

                    if memory_hits:
                        result["response"] = (
                            "הקשר מזיכרון:\n" +
                            "\n".join(
                                [x.get("question","") for x in memory_hits]
                            )
                        )
                    else:
                        mem = ima_mom.load()
                        result["response"] = ima_mom.generate_answer(
                            message,
                            mem
                        )

            except Exception as e:
                result["response"] = "IMA MASTER fallback: " + str(e)

        conversation_layer.update(
            message,
            result.get("response","")
        )

        # controlled learning event
        try:
            if len(message.strip()) > 8:
                learn_from_event({
                    "source":"user",
                    "user_id":result.get("identity",{}).get("id","default"),
                    "text":message,
                    "response":result.get("response","")
                })
        except Exception:
            pass

        return result


IMA=IMAMaster()

def ask(message):
    return IMA.ask(message)
