from pathlib import Path
import json,time,importlib.util

ROOT=Path(".ima/agi_evolution")

tests={
"memory": ROOT/"runtime"/"memory_consolidator.py",
"decision": ROOT/"runtime"/"decision_engine.py",
"planning": ROOT/"runtime"/"future_planner.py",
"evolution": ROOT/"runtime"/"self_evolution_loop.py",
"reasoning": ROOT/"reasoning"/"reasoning_engine.py",
"autonomy": ROOT/"autonomy"/"autonomy_engine.py"
}

result={
"time":time.time(),
"benchmark":{}
}

for name,path in tests.items():
    try:
        if not path.exists():
            raise Exception("missing")
        spec=importlib.util.spec_from_file_location(name,str(path))
        mod=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        result["benchmark"][name]={
            "status":"loaded",
            "path":str(path)
        }
    except Exception as e:
        result["benchmark"][name]={
            "status":"failed",
            "error":str(e)
        }

out=ROOT/"runtime"/"AGI_BENCHMARK_HISTORY.json"

history=[]
if out.exists():
    history=json.loads(out.read_text())

history.append(result)

out.write_text(
    json.dumps(history,indent=2,ensure_ascii=False)
)

print(json.dumps(result,indent=2,ensure_ascii=False))
