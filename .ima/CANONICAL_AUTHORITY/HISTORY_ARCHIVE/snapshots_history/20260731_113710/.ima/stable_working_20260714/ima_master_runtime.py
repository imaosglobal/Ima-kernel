import time
import identity_context
import conversation_layer
import ima_brain
from learning.learning_loop import learn_from_event
import ima_mom

try:
    from founder.executive_ai.integration.background_bridge import process_background
    FOUNDER_AI=True
except Exception:
    process_background=None
    FOUNDER_AI=False

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

        founder_context = None

        if FOUNDER_AI:
            try:
                founder_context = process_background(message)
            except Exception:
                founder_context = None

        result={
            "time":time.time(),
            "identity":context.get("identity",{}),
            "laws":context.get("laws",[]),
            "vision":context.get("vision",{}),
            "message":message,
            "founder_intelligence": founder_context,
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

                brain_answer = ima_brain.answer(
                    message,
                    events
                )

                if brain_answer:
                    result["response"] = brain_answer
                else:
                    memory_hits = conversation_layer.recall(message)

                    if memory_hits and len(message.strip()) > 12:
                        latest = memory_hits[-1].get("response","")
                        if latest and latest.strip() != message.strip():
                            result["response"] = latest
                        else:
                            result["response"] = ima_mom.generate_answer(
                                message,
                                ima_mom.load()
                            )
                    else:
                        result["response"] = ima_mom.generate_answer(
                            message,
                            ima_mom.load()
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
