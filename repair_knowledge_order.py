import json
from pathlib import Path
import shutil
import py_compile

p=Path("ima_master_runtime.py")

shutil.copy2(
    p,
    ".ima/backup_before_knowledge_order_repair.py"
)

lines=p.read_text(encoding="utf8").splitlines()

# אזור 142-169 לפי המבנה שנמצא
start=141   # שורה 142
end=169     # עד לפני שורה 170

replacement = '''                brain_answer=None

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
                        brain_answer=None'''

lines[start:end]=replacement.splitlines()

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
    "ביולוגיה",
    "מה זה חתול",
    "פסיכולוגיה",
    "מה הקשר בין מוזיקה ומתמטיקה"
]:
    r=m.ask(q)
    print("\nQ:",q)
    print(r.get("response","")[:500])

print("KNOWLEDGE ORDER REPAIR COMPLETE")
