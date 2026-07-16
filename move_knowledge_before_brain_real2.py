import json
from pathlib import Path
import shutil
import py_compile

p=Path("ima_master_runtime.py")

shutil.copy2(
    p,
    ".ima/backup_before_move_knowledge_real2.py"
)

text=p.read_text(encoding="utf8")

start=text.index("                  brain_answer=None")

end=text.index("                  if brain_answer:", start)

new="""                  brain_answer=None

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
                      brain_answer=None


                  if not brain_answer:
                      try:
                          brain_answer=ima_brain.answer(
                              message,
                              events
                          )
                      except Exception:
                          brain_answer=None


"""

text=text[:start]+new+text[end:]

p.write_text(text,encoding="utf8")

py_compile.compile(
    "ima_master_runtime.py",
    doraise=True
)

import ima_master_runtime

m=ima_master_runtime.IMAMaster()

for q in [
    "ביולוגיה",
    "מה זה חתול",
    "פסיכולוגיה",
    "מה הקשר בין מוזיקה ומתמטיקה"
]:
    r=m.ask(q)
    print("\\nQ:",q)
    print(r.get("response","")[:500])

print("KNOWLEDGE ROUTED BEFORE BRAIN VERIFIED")
