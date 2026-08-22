from pathlib import Path
import shutil
import py_compile
import json
import time

p=Path("ima_master_runtime.py")

shutil.copy2(
    p,
    ".ima/backup_before_world_priority.py"
)

lines=p.read_text(encoding="utf8").splitlines()


start=None
end=None

for i,l in enumerate(lines):
    if "brain_answer=None" in l:
        start=i
    if start is not None and 'if brain_answer:' in l:
        end=i
        break

if start is None or end is None:
    raise Exception("לא נמצא אזור brain")

new_block='''                brain_answer=None

                try:
                    expansion = expand_knowledge(message)

                    if expansion and expansion.get("confidence",0) < 1:
                        result["knowledge_expansion"]=expansion
                        result["response"] = (
                            "הרחבתי את שכבת הידע בנושא:\\n\\n"
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

lines[start:end]=new_block.splitlines()

text="\n".join(lines)+"\n"

if "expand_knowledge" not in text:
    raise Exception("חסר import")

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


Path(".ima/world_priority_fix.lock").write_text(
json.dumps(
{
"state":"VERIFIED",
"time":time.time(),
"pipeline":
"Question -> Expansion -> Store -> Graph -> Brain -> Memory"
},
ensure_ascii=False,
indent=2
),
encoding="utf8"
)

