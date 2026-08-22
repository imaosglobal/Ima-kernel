import json
from pathlib import Path
import shutil
import py_compile

p=Path("ima_master_runtime.py")

shutil.copy2(
    p,
    ".ima/backup_before_master_priority_order.py"
)

text=p.read_text(encoding="utf8")

old="""          try:
              if SYSTEM and hasattr(ima_system,"answer"):
                  system_result=ima_system.answer(
                      message,
                      events
                  )

                  if system_result:
                      system_answer=system_result.get("text")

          except Exception:
              system_answer=None"""

new="""          try:
              knowledge_nodes = search_concept(message)

              if knowledge_nodes:
                  result["response"]=build_answer(
                      {
                          "domain":"knowledge_graph",
                          "content":json.dumps(
                              knowledge_nodes,
                              ensure_ascii=False
                          )
                      },
                      message
                  )
                  return result

          except Exception:
              pass


          try:
              if SYSTEM and hasattr(ima_system,"answer"):
                  system_result=ima_system.answer(
                      message,
                      events
                  )

                  if system_result:
                      system_answer=system_result.get("text")

          except Exception:
              system_answer=None"""


if old not in text:
    raise Exception("SYSTEM block not found")

text=text.replace(old,new,1)

p.write_text(text,encoding="utf8")

py_compile.compile(
    "ima_master_runtime.py",
    doraise=True
)

import ima_master_runtime

m=ima_master_runtime.IMAMaster()

for q in [
    "ביולוגיה",
    "פסיכולוגיה",
    "מוזיקה"
]:
    r=m.ask(q)

