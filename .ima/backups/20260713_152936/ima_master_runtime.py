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
            memory_hits = conversation_layer.recall(message)

            if memory_hits:
                result["response"] = "זיכרון רלוונטי:\n" + "\n".join(
                    [x.get("question","") for x in memory_hits]
                )
            else:
                result["response"]="IMA MASTER: "+message

        conversation_layer.update(
            message,
            result.get("response","")
        )
        return result


IMA=IMAMaster()

def ask(message):
    return IMA.ask(message)
