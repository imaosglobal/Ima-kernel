from pathlib import Path
import json,time

import conversation_layer
import identity_context

try:
    import ima_brain
except:
    ima_brain=None

try:
    import ima_system
except:
    ima_system=None


class IMACore:

    def __init__(self):
        self.name="IMA CORE"
        self.version="fusion-1"

    def process(self,message):

        conversation_layer.update(message)

        context=identity_context.build_context(message)

        result={
            "time":int(time.time()),
            "identity":context.get("identity",{}),
            "laws":context.get("laws",[]),
            "vision":context.get("vision",{}),
            "message":message
        }

        if "מי אני" in message:
            result["response"]=context.get("legacy","")

        elif "חוקים" in message:
            result["response"]="\n".join(context.get("laws",[]))

        elif "המטרה של IMA" in message or "מטרת IMA" in message or "למה IMA" in message:
            vision=context.get("vision",{})
            result["response"]=vision.get("goal","") + "\n\n" + vision.get("belief","")

        else:
            result["response"]="IMA קיבלה: "+message

        return result


CORE=IMACore()


def ask(message):
    return CORE.process(message)
