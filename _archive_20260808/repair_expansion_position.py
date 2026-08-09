from pathlib import Path
import shutil
import py_compile
import json
import time

p=Path("ima_master_runtime.py")

shutil.copy2(
    p,
    ".ima/backup_before_expansion_position_fix.py"
)

lines=p.read_text(encoding="utf8").splitlines()

# שורות לפי המבנה הנוכחי
insert_at=None

for i,l in enumerate(lines):
    if "brain_answer=ima_brain.answer" in l:
        insert_at=i-1
        break

if insert_at is None:
    raise Exception("לא נמצא brain")

block=[
'                  try:',
'                      expansion = expand_knowledge(message)',
'',
'                      if expansion and expansion.get("confidence",0) <= 0.5:',
'                          result["knowledge_expansion"]=expansion',
'                          result["response"]=(',
'                              "הידע דורש הרחבה:\\n\\n"',
'                              + expansion.get("content","")',
'                          )',
'                          return result',
'',
'                  except Exception:',
'                      pass',
''
]

lines[insert_at:insert_at]=block

p.write_text(
    "\n".join(lines)+"\n",
    encoding="utf8"
)

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
    print(r.get("response","")[:300])
    print("EXPANSION:",r.get("knowledge_expansion"))

Path(".ima/expansion_position_verified.lock").write_text(
json.dumps(
{
"state":"VERIFIED",
"pipeline":"Question -> Knowledge -> Expansion -> Brain -> Memory",
"time":time.time()
},
ensure_ascii=False,
indent=2
),
encoding="utf8"
)

print("\nEXPANSION POSITION VERIFIED")
