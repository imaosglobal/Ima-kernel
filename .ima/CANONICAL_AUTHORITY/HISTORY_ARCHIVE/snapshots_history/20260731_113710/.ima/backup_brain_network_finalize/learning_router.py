
from learning.learning_memory import store_pattern

def route_learning(event):

    source = event.get("source","user")

    if source == "user":
        return {
            "route":"user_memory",
            "action":"learn_user"
        }

    if source == "ima":
        return {
            "route":"self_learning",
            "action":"learn_self"
        }

    return {
        "route":"world_memory",
        "action":"learn_world"
    }
