import json
import time
import importlib.util
from pathlib import Path

ROOT=Path(".ima/agi_evolution").resolve()

tests={
    "agi_orchestrator": ROOT/"runtime/agi_orchestrator.py",
    "agi_bridge": ROOT/"runtime/ima_agi_bridge.py",
    "reasoning": ROOT/"reasoning/reasoning_engine.py",
    "autonomy": ROOT/"autonomy/autonomy_engine.py",
    "persona": ROOT/"persona_engine/persona_engine.py",
    "self_improvement": ROOT/"self_improvement/self_improvement_engine.py"
}

result={
    "time":time.time(),
    "tests":{}
}

for name,path in tests.items():
    try:
        if not path.exists():
            raise Exception("missing file")

        spec=importlib.util.spec_from_file_location(name,str(path))
        mod=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        result["tests"][name]={
            "status":"loaded",
            "path":str(path)
        }

    except Exception as e:
        result["tests"][name]={
            "status":"failed",
            "error":str(e),
            "path":str(path)
        }

Path(".ima/agi_evolution/runtime/reality_capability_test.json").write_text(
    json.dumps(result,indent=2,ensure_ascii=False)
)

print(json.dumps(result,indent=2,ensure_ascii=False))
