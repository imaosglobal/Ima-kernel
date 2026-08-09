import time

CURRENT_VERSION="1.0"

def status():
    return {
        "version": CURRENT_VERSION,
        "update_ready": True,
        "rollback": True,
        "time": time.time()
    }
