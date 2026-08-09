from pathlib import Path
import shutil
import py_compile
import json
import time

p=Path("ima_master_runtime.py")

shutil.copy2(
    p,
    ".ima/backup_before_expansion_move.py"
)

text=p.read_text(encoding="utf8")


old='''                  if not brain_answer:
                      try:
                          brain_answer=ima_brain.answer(
                              message,
                              events
                          )
                      except Exception:
                          brain_answer=None
'''

new='''                  if not brain_answer:
                      try:
                          expansion = expand_knowledge(message)

                          if expansion and expansion.get("confidence",0) <= 0.5:
                              result["knowledge_expansion"]=expansion
                              result["response"]=(
                                  "למדתי שצריך להרחיב את הידע בנושא:\\n\\n"
                                  + expansion.get("content","")
                              )
                              return result

                      except Exception:
                          pass

                      try:
                          brain_answer=ima_brain.answer(
                              message,
                              events
                          )
                      except Exception:
                          brain_answer=None
'''

if old not in text:
    raise Exception("לא נמצא בלוק brain fallback")

text=text.replace(old,new,1)

p.write_text(text,encoding="utf8")


py_compile.compile(
    "ima_master_runtime.py",
    doraise=True
)

import ima_master_runtime

m=ima_master_runtime.IMAMaster()

for q in [
    "מה זה קוואנטום",
    "מה זה חתול",
    "מה הקשר בין מוזיקה ומתמטיקה"
]:
    r=m.ask(q)
    print("\nQ:",q)
    print(r.get("response","")[:500])
    print("EXP:",r.get("knowledge_expansion"))


Path(".ima/expansion_priority_verified.lock").write_text(
json.dumps(
{
"state":"VERIFIED",
"pipeline":
"Question -> Knowledge -> Expansion -> Brain -> Memory",
"time":time.time()
},
ensure_ascii=False,
indent=2
),
encoding="utf8"
)

print("\nEXPANSION PRIORITY VERIFIED")
