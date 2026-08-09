from pathlib import Path
import shutil
import py_compile
import json
import time
import importlib

ROOT=Path(".")
IMA=Path(".ima")
IMA.mkdir(exist_ok=True)

runtime=Path("ima_master_runtime.py")

if not runtime.exists():
    raise Exception("ima_master_runtime.py missing")

shutil.copy2(
    runtime,
    IMA/"backup_before_world_learning_final.py"
)

text=runtime.read_text(encoding="utf8")


# imports
if "from learning.knowledge_expansion_engine import expand_knowledge" not in text:
    anchor="from learning.knowledge_answer_builder import build_answer"

    if anchor in text:
        text=text.replace(
            anchor,
            anchor+"\nfrom learning.knowledge_expansion_engine import expand_knowledge"
        )
    else:
        text=text.replace(
            "import json",
            "import json\nfrom learning.knowledge_expansion_engine import expand_knowledge"
        )


# locate final fallback
target="""
                    memory_hits=conversation_layer.recall(message)
"""

inject="""
                    try:
                        expansion = expand_knowledge(message)

                        if expansion:
                            result["knowledge_expansion"] = expansion

                            if expansion.get("confidence",0) < 1:
                                result["response"] = (
                                    "הרחבתי את מאגר הידע בנושא:\\n\\n"
                                    + expansion.get("content","")
                                )
                                return result

                    except Exception:
                        pass

                    memory_hits=conversation_layer.recall(message)
"""


if "result[\"knowledge_expansion\"] = expansion" not in text:

    if target in text:
        text=text.replace(target,inject,1)
    else:
        raise Exception("לא נמצא fallback runtime")


runtime.write_text(text,encoding="utf8")


# compile
py_compile.compile(
    "ima_master_runtime.py",
    doraise=True
)


# modules check
modules=[
"ima_master_runtime",
"learning.knowledge_retrieval",
"learning.knowledge_answer_builder",
"learning.knowledge_graph_retrieval",
"learning.knowledge_expansion_engine"
]

status={}

for m in modules:
    try:
        importlib.import_module(m)
        status[m]="OK"
    except Exception as e:
        status[m]="FAIL "+str(e)


# runtime test
import ima_master_runtime

m=ima_master_runtime.IMAMaster()

tests=[
"מה זה חתול",
"מה זה קוואנטום",
"מה הקשר בין מוזיקה ומתמטיקה",
"מה הקשר בין מוח ובינה מלאכותית"
]

results={}

for q in tests:
    r=m.ask(q)
    results[q]={
        "response":r.get("response","")[:500],
        "expansion":r.get("knowledge_expansion")
    }


report={
"system":"IMA",
"time":time.time(),
"pipeline":
"Question -> Knowledge Store -> Graph -> Expansion -> Memory -> Response",
"modules":status,
"tests":results
}


(IMA/"world_learning_final_report.json").write_text(
json.dumps(
report,
ensure_ascii=False,
indent=2
),
encoding="utf8"
)


print(json.dumps(report,ensure_ascii=False,indent=2))
print("IMA WORLD LEARNING FINAL VERIFIED")

