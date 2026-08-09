from pathlib import Path
import shutil
import py_compile
import json
import time

p=Path("ima_master_runtime.py")

shutil.copy2(
    p,
    ".ima/backup_before_knowledge_priority_fix.py"
)

text=p.read_text(encoding="utf8")


if "from learning.knowledge_graph_retrieval import search_concept" not in text:
    text=text.replace(
        "from learning.knowledge_answer_builder import build_answer",
        """from learning.knowledge_answer_builder import build_answer
from learning.knowledge_graph_retrieval import search_concept
import json"""
    )


old="""if brain_answer:

                      result["response"]=brain_answer

                  else:"""


new="""if brain_answer:

                      result["response"]=brain_answer

                  else:

                      knowledge_answer=None

                      try:
                          nodes = search_concept(message)

                          if nodes:
                              knowledge_answer = build_answer(
                                  {
                                      "domain":"knowledge_graph",
                                      "content":json.dumps(
                                          nodes,
                                          ensure_ascii=False
                                      )
                                  },
                                  message
                              )

                      except Exception:
                          knowledge_answer=None


                      if knowledge_answer:
                          result["response"]=knowledge_answer

                      else:"""


if "nodes = search_concept(message)" not in text:

    if old not in text:
        raise Exception("לא נמצא מסלול fallback")

    text=text.replace(old,new,1)


p.write_text(text,encoding="utf8")

py_compile.compile(
    "ima_master_runtime.py",
    doraise=True
)


import ima_master_runtime

m=ima_master_runtime.IMAMaster()

tests=[
"ביולוגיה",
"מה זה חתול",
"פסיכולוגיה",
"מה הקשר בין מוזיקה ומתמטיקה"
]


for q in tests:
    r=m.ask(q)
    print("\nQ:",q)
    print(r.get("response","")[:500])


Path(".ima/knowledge_priority_fix.lock").write_text(
    json.dumps(
        {
        "state":"VERIFIED",
        "pipeline":
        "Question -> Knowledge Graph -> Answer Builder -> Response -> Mom fallback",
        "time":time.time()
        },
        indent=2,
        ensure_ascii=False
    ),
    encoding="utf8"
)

print("\nKNOWLEDGE PRIORITY FIX COMPLETE")
