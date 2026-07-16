from pathlib import Path
import shutil
import time
import json
import py_compile

runtime = Path("ima_master_runtime.py")

backup = Path(".ima/backup_before_universal_pipeline.py")
shutil.copy2(runtime, backup)

text = runtime.read_text(encoding="utf8")

if "knowledge_graph_retrieval" not in text:

    text = text.replace(
        "from learning.knowledge_answer_builder import build_answer",
        """from learning.knowledge_answer_builder import build_answer
from learning.knowledge_graph_retrieval import search_concept"""
    )


marker = """brain_answer=ima_brain.answer(
                        message,
                        events
                    )"""

inject = """brain_answer=ima_brain.answer(
                        message,
                        events
                    )

                    if not brain_answer:
                        try:
                            knowledge_nodes = search_concept(message)

                            if knowledge_nodes:
                                brain_answer = build_answer(
                                    {
                                    "domain":"knowledge_graph",
                                    "content":json.dumps(
                                        knowledge_nodes,
                                        ensure_ascii=False
                                    )
                                    },
                                    message
                                )

                        except Exception:
                            pass"""


if "knowledge_nodes = search_concept" not in text:

    if marker in text:
        text=text.replace(marker,inject,1)
    else:
        raise Exception("לא נמצא מקום חיבור Brain")


runtime.write_text(text,encoding="utf8")


py_compile.compile(
    "ima_master_runtime.py",
    doraise=True
)


import ima_master_runtime

m=ima_master_runtime.IMAMaster()


tests=[
"ביולוגיה",
"פסיכולוגיה",
"מה הקשר בין מוזיקה ומתמטיקה",
"מה הקשר בין מוח ובינה מלאכותית",
"מה הקשר בין פיזיקה והנדסה"
]


results={}

for q in tests:
    r=m.ask(q)
    results[q]=r.get("response","")[:500]


Path(".ima/universal_pipeline_report.json").write_text(
    json.dumps(
        {
        "time":time.time(),
        "pipeline":
        "Question -> Knowledge Graph -> Retrieval -> Answer Builder -> Response",
        "tests":results
        },
        ensure_ascii=False,
        indent=2
    ),
    encoding="utf8"
)


print(json.dumps(results,ensure_ascii=False,indent=2))
print("UNIVERSAL KNOWLEDGE PIPELINE CONNECTED")
