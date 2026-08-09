import json
import time
import identity_context
import conversation_layer
import ima_brain

try:
    import sys
    sys.path.insert(0,'.ima')
    import autonomy_context
except Exception:
    autonomy_context=None
from learning.knowledge_answer_builder import build_answer

# IMA cognitive layers
try:
    from truth_engine import evaluate_truth
except Exception:
    evaluate_truth=None

try:
    from ima_question_engine import generate_question
except Exception:
    generate_question=None

from learning.knowledge_expansion_engine import expand_knowledge
from learning.knowledge_graph_retrieval import search_concept
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


from connectors.llm.router import ask_models
from skills.router import choose
from skills.intent import detect
from memory.context import get_context, store_interaction
from connectors.llm.ima_pipeline import ask as ima_llm_answer
from connectors.llm.auto_runtime import run as auto_llm_run

class IMAMaster:

    def __init__(self):
        self.name="IMA MASTER"

    def ask(self,message):
        llm_models = ask_models(message)

        memory_context = get_context()

        intent = detect(message)

        skill_context = choose(
            intent,
            message
        )

        llm_pipeline_result = ima_llm_answer(
            message
        )
        auto_llm = auto_llm_run(message)

        external_models = ask_models(message)


        system_learning_context = {}

        try:
            if autonomy_context:
                system_learning_context = autonomy_context.load_context()
        except Exception:
            system_learning_context = {}

        learning_hint = ""

        try:
            lessons = system_learning_context.get("lessons", [])
            if lessons:
                latest = lessons[-3:]
                learning_hint = "\n\nלקחי מערכת אחרונים:\n" + "\n".join(
                    [
                        str(x.get("lesson",x))
                        for x in latest
                    ]
                )
        except Exception:
            pass



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
            "auto_llm": auto_llm,
        "skill_context": skill_context,
        "memory_context": memory_context,
        "memory_saved": None,
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

                # rank memory quality
                def memory_score(x):
                    r=x.get("response","")
                    q=x.get("question","")

                    score=0

                    if "אני כאן כדי להקשיב" in r:
                        score-=10
                    else:
                        score+=5

                    if "אני נבנית מזיכרון" in r:
                        score+=8

                    if len(r)>100 and "אני כאן כדי להקשיב" not in r:
                        score+=2

                    if len(q)>5:
                        score+=1

                    return score


                memory_hits=sorted(
                    memory_hits,
                    key=memory_score,
                    reverse=True
                )

                memory_hits=memory_hits[:5]

                if memory_hits:
                    result["response"]="\n\n".join(
                        [
                            f"אתה: {x.get('question','')}\nIMA: {x.get('response','')[:300]}"
                            for x in memory_hits[-10:]
                            if x.get("response")
                            and "fallback" not in x.get("response","")
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
                    knowledge_nodes = search_concept(message)

                    if knowledge_nodes:
                        brain_answer = build_answer(
                            {
                                "domain":"knowledge_graph",
                                "content":json.dumps(
                                    knowledge_nodes,
                                    ensure_ascii=False
                                )
                            },
                            message
                        )
                    else:
                        brain_answer=None

                except Exception:
                    brain_answer=None


                if not brain_answer:
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

                    try:
                        expansion = expand_knowledge(message)

                        if expansion:
                            result["knowledge_expansion"] = expansion

                    except Exception:
                        pass

                    memory_hits=conversation_layer.recall(message)

                    memory_hits=[
                        x for x in memory_hits
                        if x.get("response")
                        and "אני כאן כדי להקשיב" not in x.get("response","")
                        and "fallback" not in x.get("response","")
                    ]

                    memory_hits=[
                        x for x in memory_hits
                        if x.get("response")
                        and "לא מצאתי" not in x.get("response","")
                        and "fallback" not in x.get("response","")
                    ]

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

                store_result = store_interaction(
                    message,
                    result.get("response","")
                )

                result["memory_saved"] = store_result

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




        # === IMA AGI EVOLUTION INTEGRATION ===
        try:
            from pathlib import Path
            import sys

            agi_root=Path(".ima/agi_evolution").resolve()
            if str(agi_root) not in sys.path:
                sys.path.insert(0,str(agi_root))

            from runtime.ima_agi_bridge import IMA_AGI

            agi_result=IMA_AGI.process(
                message,
                {
                    "identity":"active",
                    "memory":"active",
                    "learning":"active"
                }
            )

            result["agi"]=agi_result

        except Exception as e:
            result["agi_error"]=str(e)

        return result



IMA=IMAMaster()


def ask(message):

    return IMA.ask(message)
