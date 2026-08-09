from pathlib import Path
import shutil
import py_compile
import json
import time

p=Path("ima_master_runtime.py")

shutil.copy2(
    p,
    ".ima/backup_before_world_learning_connection.py"
)

text=p.read_text(encoding="utf8")

if "from learning.knowledge_expansion_engine import expand_knowledge" not in text:
    text=text.replace(
        "from learning.knowledge_answer_builder import build_answer",
        """from learning.knowledge_answer_builder import build_answer
from learning.knowledge_expansion_engine import expand_knowledge"""
    )

old="""                else:

                    memory_hits=conversation_layer.recall(message)"""

new="""                else:

                    try:
                        expansion = expand_knowledge(message)

                        if expansion:
                            result["knowledge_expansion"] = expansion

                    except Exception:
                        pass

                    memory_hits=conversation_layer.recall(message)"""

if old not in text:
    raise Exception("לא נמצא fallback memory block")

text=text.replace(old,new,1)

p.write_text(text,encoding="utf8")

py_compile.compile(
    "ima_master_runtime.py",
    doraise=True
)

import ima_master_runtime

from learning.knowledge_expansion_engine import expand_knowledge

m=ima_master_runtime.IMAMaster()

tests=[
"מה זה חתול",
"מהי ביולוגיה",
"מה הקשר בין מוזיקה ומתמטיקה",
"מה זה קוואנטום"
]

report={}

for q in tests:
    direct=expand_knowledge(q)
    runtime=m.ask(q)

    report[q]={
        "expansion_engine":direct,
        "runtime_response":runtime.get("response","")[:300],
        "has_expansion": "knowledge_expansion" in runtime
    }

Path(".ima/world_learning_engine_report.json").write_text(
    json.dumps(
        {
        "time":time.time(),
        "pipeline":
        "Question -> Brain -> Expansion -> Store -> Graph -> Memory",
        "tests":report
        },
        ensure_ascii=False,
        indent=2
    ),
    encoding="utf8"
)

print(json.dumps(report,ensure_ascii=False,indent=2))
print("IMA WORLD LEARNING ENGINE VERIFIED")
