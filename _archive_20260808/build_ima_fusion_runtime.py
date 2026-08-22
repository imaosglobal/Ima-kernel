from pathlib import Path
import json
import time

ROOT = Path(".")
REPORT = ROOT / ".ima" / "reports"
REPORT.mkdir(parents=True, exist_ok=True)


# 1. יצירת שכבת Fusion
fusion = ROOT / "ima_fusion_runtime.py"

fusion.write_text(
'''import time
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
''',
encoding="utf-8"
)



# 2. תיקון ima_core_router.py
router = ROOT / "ima_core_router.py"

if router.exists():

    text = router.read_text(encoding="utf-8")

    old = '''        try:
            core["mother_connected"] = True
        except:
            core["mother_connected"] = False'''

    new = '''        try:
            import ima_mom
            core["mother_connected"] = True
            core["mother_layer"] = ima_mom.__name__
        except Exception:
            core["mother_connected"] = False'''

    if old in text:
        text = text.replace(old,new)
        router.write_text(text,encoding="utf-8")

    else:


# 3. בדיקת מצב
status_file = REPORT / "fusion_runtime_status.json"

try:
    import importlib
    fusion_module = importlib.import_module("ima_fusion_runtime")
    status = fusion_module.fusion_status()
except Exception as e:
    status = {
        "status":"error",
        "error":str(e)
    }


status_file.write_text(
    json.dumps(
        status,
        ensure_ascii=False,
        indent=2
    ),
    encoding="utf-8"
)



for layer,data in status.get("layers",{}).items():
        layer,
        "OK" if data.get("connected") else "FAILED"
    )

