from languages.language_engine import detect_language
from languages.translator import translate_response
import json
import re
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

# ============================================================
# IMA SELF AWARENESS SYSTEM QUERY
# ============================================================
try:
    from self_awareness.system_query import format_status
    SELF_AWARENESS=True
except Exception:
    format_status=None
    SELF_AWARENESS=False

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
        language = detect_language(message)

        # ============================================================
        # CANONICAL MEMORY PRIORITY GATE
        # ============================================================
        # Memory requests terminate before any expensive model execution.
        # ============================================================

        result = {
            "time": time.time(),
            "message": message,
            "memory_saved": None,
            "connections": {
                "memory": True,
                "brain": True,
                "system": SYSTEM
            }
        }

        # ============================================================
        # SELF AWARENESS SYSTEM COMMANDS
        # ============================================================

        system_commands = [
            "מה מצב המערכת",
            "מצב המערכת",
            "סטטוס",
            "בריאות המערכת",
            "health",
            "status",
            "בדיקה עצמית",
        ]

        if SELF_AWARENESS and any(
            cmd.lower() in message.lower()
            for cmd in system_commands
        ):
            result["response"] = format_status()
            return result

        memory_commands = [
            "מה דיברנו",
            "מה דיברנו קודם",
            "תזכיר לי",
            "מה אתה זוכר",
            "מה את זוכרת",
            "היסטוריה",
        ]

        is_memory_request = any(
            command in message
            for command in memory_commands
        )

        if is_memory_request:
            try:
                memory_hits = conversation_layer.recall(message)

                memory_hits = [
                    x for x in memory_hits
                    if x.get("response")
                    and "fallback" not in x.get("response", "")
                    and "אני כאן כדי להקשיב" not in x.get("response", "")
                    and "לא מצאתי" not in x.get("response", "")
                ]

                    # Strong relevance filter
                stopwords = {
                    "מה", "אתה", "את", "אני", "היא", "הוא",
                    "זוכר", "זוכרת", "דיברנו", "קודם", "על",
                    "אתם", "היסטוריה", "תזכיר", "לי"
                }

                query_terms = [
                    t.strip("?!.,:;()[]{}")
                    for t in message.split()
                    if len(t.strip("?!.,:;()[]{}")) >= 5
                    and t.strip("?!.,:;()[]{}") not in stopwords
                ]

                exact_hits = [
                    x for x in memory_hits
                    if any(
                        t in x.get("question", "")
                        or t in x.get("response", "")
                        for t in query_terms
                    )
                ]

                if query_terms:
                    memory_hits = exact_hits

                def memory_score(x):
                    question = x.get("question", "")
                    response = x.get("response", "")
                    score = 0

                    query_terms = [
                        t for t in message.split()
                        if len(t) >= 4
                    ]

                    score += sum(
                        100 for t in query_terms
                        if t == question or t == response
                        or t in question.split()
                        or t in response.split()
                    )

                    if len(question) > 5:
                        score += 1
                    if len(response) > 100:
                        score += 2
                    if "אני נבנית מזיכרון" in response:
                        score += 8

                    return score

                                # Remove duplicate memories by question
                unique = {}
                for x in memory_hits:
                    q = x.get("question", "").strip()
                    if q:
                        unique[q] = x
                memory_hits = list(unique.values())

                memory_hits = sorted(
                    memory_hits,
                    key=memory_score,
                    reverse=True
                )[:1]

                if memory_hits:
                    result["response"] = "\n\n".join(
                        f"אתה: {x.get('question', '')}\n"
                        f"IMA: {x.get('response', '')[:500]}"
                        for x in memory_hits
                    )
                else:
                    result["response"] = (
                        "אין זיכרון מתאים נמצא ב-Supabase או בזיכרון המקומי."
                    )

                result['response'] = translate_response(result.get('response',''), language)
                return result

            except Exception as memory_error:
                result["memory_error"] = str(memory_error)
                result["response"] = (
                    "לא הצלחתי לקרוא את זיכרון השיחה כרגע."
                )
                return result


        llm_models = ask_models(message)

        memory_context = get_context()

        # DIRECT_MEMORY_PATCH
        direct_memory = memory_direct_answer(
            message,
            memory_context
        )

        if direct_memory:
            return {
                "time": time.time(),
                "message": message,
                "response": direct_memory,
                "memory_context": memory_context,
                "connections": {
                    "memory": True,
                    "brain": True
                }
            }
        # END_DIRECT_MEMORY_PATCH



        direct_memory = memory_direct_answer(
            message,
            memory_context
        )

        if direct_memory:
            return {
                "time":time.time(),
                "message":message,
                "response":direct_memory,
                "memory_context":memory_context,
                "connections":{
                    "memory":True,
                    "brain":True
                }
            }





        # FORCE_MEMORY_PRIORITY_FIXED

        def deep_find_preferences(obj):
            found=[]

            if isinstance(obj,dict):
                for k,v in obj.items():

                    if k=="preference":
                        if isinstance(v,dict):
                            value=v.get("value","")
                            if value:
                                found.append(str(value))
                        elif v:
                            found.append(str(v))

                    found.extend(
                        deep_find_preferences(v)
                    )

            elif isinstance(obj,list):
                for item in obj:
                    found.extend(
                        deep_find_preferences(item)
                    )

            return found


        forced_prefs=deep_find_preferences(
            memory_context
        )


        if "מה אני אוהב" in message and forced_prefs:

            clean_pref=[]

            for x in forced_prefs:
                if x not in clean_pref:
                    clean_pref.append(x)

            return {
                "time":time.time(),
                "message":message,
                "response":
                    "אני זוכרת שאתה אוהב "
                    + ", ".join(clean_pref),
                "memory_context":memory_context,
                "connections":{
                    "memory":True,
                    "brain":True,
                    "mother":True
                }
            }

        # END_FORCE_MEMORY_PRIORITY



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

                try:
                    from api.database.memory_store import load_memory
                    supabase_memories = load_memory()

                    if supabase_memories:
                        result["response"] = "\n".join(
                            x.get("content", "")
                            for x in supabase_memories[-5:]
                            if x.get("content", "")
                        )
                    elif memory_hits:
                        result["response"] = "\n".join(
                            x.get("question", "").strip()
                            for x in memory_hits
                            if x.get("question", "").strip()
                        )
                    else:
                        result["response"]="אין זיכרון מתאים נמצא ב-Supabase או בזיכרון המקומי."
                except Exception:
                    result["response"]="אין זיכרון מתאים נמצא ב-Supabase או בזיכרון המקומי."

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





def clean_ima_response(text):
    if not isinstance(text,str):
        return text

    markers=[
        "הקשר משתמש:",
        "הודעת משתמש:",
        "USER CONTEXT:",
        "זיכרון משתמש:"
    ]

    for marker in markers:
        if marker in text:
            text=text.split(marker)[0]

    return text.strip()





def memory_direct_answer(message, memory):
    if not isinstance(message,str):
        return None

    m=message.strip()

    prefs=[]

    try:
        if isinstance(memory,dict):
            for k,v in memory.items():
                if k=="preference":
                    if isinstance(v,dict):
                        prefs.append(str(v.get("value","")))
                    else:
                        prefs.append(str(v))
    except Exception:
        pass

    if "מה אני אוהב" in m and prefs:
        return "אני זוכרת שאתה אוהב " + ", ".join(prefs)

    return None





def sanitize_memory_write(text):
    if not isinstance(text,str):
        return text

    bad=[
        "זיכרון משתמש:",
        "הקשר משתמש:",
        "הודעת משתמש:",
        "USER CONTEXT:",
        "Memory:",
        "את IMA.",
    ]

    for marker in bad:
        if marker in text:
            text=text.split(marker)[0]

    return text.strip()



IMA=IMAMaster()


def ask(message):

    return IMA.ask(message)
