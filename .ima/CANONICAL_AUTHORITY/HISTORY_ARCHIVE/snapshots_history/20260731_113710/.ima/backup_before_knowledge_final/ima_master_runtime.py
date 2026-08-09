import time
import identity_context
import conversation_layer
import ima_brain
from learning.knowledge_answer_builder import build_answer
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
except Exception:
    SYSTEM=False


class IMAMaster:

    def __init__(self):
        self.name="IMA MASTER"

    def ask(self,message):

        context=identity_context.build_context(message)

        intent=None
        emotion=None

        try:
            if hasattr(ima_system,"detect_intent"):
                intent=ima_system.detect_intent(message)
        except Exception:
            pass

        try:
            if hasattr(ima_system,"ima_emotion_layer"):
                emotion=ima_system.ima_emotion_layer(message,[])
        except Exception:
            pass

        founder_context=None

        if FOUNDER_AI:
            try:
                founder_context=process_background(message)
            except Exception:
                pass

        result={
            "time":time.time(),
            "identity":context.get("identity",{}),
            "laws":context.get("laws",[]),
            "vision":context.get("vision",{}),
            "message":message,
            "intent":intent,
            "emotion":emotion,
            "founder_intelligence":founder_context,
            "connections":{
                "identity":True,
                "memory":True,
                "brain":True,
                "mother":True,
                "system":SYSTEM
            }
        }


        memory_commands=[
            "מה דיברנו",
            "מה דיברנו קודם",
            "תזכיר לי",
            "מה אתה זוכר",
            "מה את זוכרת",
            "היסטוריה"
        ]


        if "מי אני" in message:
            result["response"]=context.get("legacy","")
            return result

        if "חוקים" in message:
            result["response"]="\n".join(context.get("laws",[]))
            return result

        if "מטרה" in message or "חזון" in message:
            result["response"]=(
                context.get("vision",{}).get("goal","")
                + "\n\n" +
                context.get("vision",{}).get("belief","")
            )
            return result


        try:
            events=ima_brain.load_events()

            if any(x in message for x in memory_commands):

                memory_hits=conversation_layer.recall("")

                if memory_hits:
                    result["response"]="\n\n".join(
                        [
                            f"אתה: {x.get('question','')}\nIMA: {x.get('response','')[:300]}"
                            for x in memory_hits
                        ]
                    )
                else:
                    result["response"]="עדיין אין לי מספיק זיכרון שיחה למצוא."

                return result
            system_answer=None

            try:
                if SYSTEM and hasattr(ima_system,"answer"):
                    system_result=ima_system.answer(
                        message,
                        events
                    )

                    if system_result:
                        system_answer=system_result.get("text")

            except Exception:
                system_answer=None


            if system_answer:

                result["response"]=system_answer

            else:

                brain_answer=None

                try:
                    brain_answer=ima_brain.answer(
                        message,
                        events
                    )
                except Exception:
                    brain_answer=None


                if brain_answer:

                    result["response"]=brain_answer

                else:

                    memory_hits=conversation_layer.recall(message)

                    if memory_hits and len(message.strip()) > 12:

                        latest=memory_hits[-1].get("response","")

                        if latest and latest.strip()!=message.strip():
                            result["response"]=latest
                        else:
                            result["response"]=ima_mom.generate_answer(
                                message,
                                ima_mom.load()
                            )

                    else:

                        result["response"]=ima_mom.generate_answer(
                            message,
                            ima_mom.load()
                        )


        except Exception as e:

            result["response"]="IMA MASTER fallback: " + str(e)



        try:

            if not any(x in message for x in memory_commands):

                conversation_layer.update(
                    message,
                    result.get("response","")
                )

        except Exception:
            pass



        try:

            if len(message.strip()) > 8:

                event = {
                    "source":"user",
                    "user_id":result.get("identity",{}).get("id","default"),
                    "text":message,
                    "response":result.get("response","")
                }

                learn_from_event(event)

                try:
                    import brain_sync
                    brain_sync.broadcast({
                        "type":"LEARNING_EVENT",
                        "event":event,
                        "time":time.time()
                    })
                except Exception:
                    pass

        except Exception:
            pass



        return result



IMA=IMAMaster()


def ask(message):

    return IMA.ask(message)
