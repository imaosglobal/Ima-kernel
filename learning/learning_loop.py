from learning.runtime_bridge import emit_learning_event
from learning.learning_router import route_learning
from learning.self_learning import learn_self
from learning.user_memory import learn
from learning.world_memory import store
from learning.learning_gate import should_learn
from learning.skill_compiler import compile_and_record
from learning.learning_gap_detector import record as record_learning_gap
import time


def process_event(event):
    if not should_learn(event):
        return {"status":"ignored","reason":"learning_gate"}

    route = route_learning(event)

    if route["route"] == "user_memory":
        return learn(event.get("user_id","default"), event)

    if route["route"] == "self_learning":
        return learn_self(event.get("text",""))

    return store(event.get("topic","general"), event)


def learn_from_event(event):
    if not should_learn(event):
        return {
            "time": time.time(),
            "route": "blocked",
            "result": {"status":"ignored","reason":"learning_gate"},
            "status":"ignored"
        }

    result = process_event(event)

    skill = None
    gap = None
    try:
        skill = compile_and_record(event)
    except Exception as exc:
        skill = {"status":"error","error":str(exc)}

    try:
        gap = record_learning_gap(event)
    except Exception as exc:
        gap = {"status":"error","error":str(exc)}

    return {
        "time": time.time(),
        "route": route_learning(event),
        "result": result,
        "applied_skill": skill,
        "learning_gap": gap,
        "status": "processed"
    }
