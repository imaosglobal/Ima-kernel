import time
import json

STATUS = {
    "identity": "IMA Fusion Runtime",
    "created": time.time()
}


def safe_import(name):
    try:
        module = __import__(name)
        return {
            "name": name,
            "connected": True,
            "module": module
        }
    except Exception as e:
        return {
            "name": name,
            "connected": False,
            "error": str(e)
        }


LAYERS = {
    "master_runtime": safe_import("ima_master_runtime"),
    "core_router": safe_import("ima_core_router"),
    "self_knowledge": safe_import("ima_self_knowledge_bridge"),
    "system": safe_import("ima_system"),
    "learning": safe_import("learning.meta_orchestrator")
}


def fusion_status():
    return {
        "identity": STATUS,
        "layers": {
            k: {
                "connected": v.get("connected"),
                "error": v.get("error")
            }
            for k,v in LAYERS.items()
        }
    }


def process(message):
    try:
        router = LAYERS["core_router"]

        if router.get("connected"):
            return router["module"].ask(message)

    except Exception:
        pass

    try:
        master = LAYERS["master_runtime"]

        if master.get("connected"):
            return master["module"].ask(message)

    except Exception as e:
        return {
            "response": "IMA Fusion fallback",
            "error": str(e)
        }


    return {
        "response": "IMA Fusion received: " + message
    }
