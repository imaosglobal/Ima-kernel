import time
import identity_context
import conversation_layer
import ima_brain
import ima_mom

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
        return result


IMA=IMAMaster()

def ask(message):
    return IMA.ask(message)
