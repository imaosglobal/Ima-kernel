import time

ENABLED=False

def ask(prompt):
    if not ENABLED:
        return {
            "model":"local_disabled",
            "response":"",
            "status":"disabled",
            "time":time.time()
        }

    return {
        "model":"local_disabled",
        "response":"",
        "status":"not_available",
        "time":time.time()
    }
