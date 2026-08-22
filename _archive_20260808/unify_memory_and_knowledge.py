from pathlib import Path
import json
import shutil
import time

ROOT = Path(".")
MEM = ROOT / "learning/learning_memory.json"
PAT = ROOT / "learning/learning_patterns.json"

BACKUP = ROOT / ".ima/backup_memory_knowledge_merge"
BACKUP.mkdir(parents=True, exist_ok=True)

# backup
for f in [MEM, PAT, ROOT/"ima_master_runtime.py"]:
    if f.exists():
        shutil.copy2(
            f,
            BACKUP / f.name
        )



# merge memories
memory = {}

if MEM.exists():
    memory = json.loads(
        MEM.read_text(encoding="utf8")
    )

patterns=[]

if PAT.exists():
    p=json.loads(
        PAT.read_text(encoding="utf8")
    )
    patterns=p.get("patterns",[])

existing = {
    x.get("pattern")
    for x in memory.get("patterns",[])
}

for item in patterns:
    if item.get("pattern") not in existing:
        memory.setdefault("patterns",[]).append(item)

memory["memory_unified"]=True
memory["merged_from_pattern_memory"]=True
memory["merge_time"]=time.time()


MEM.write_text(
    json.dumps(
        memory,
        ensure_ascii=False,
        indent=2
    ),
    encoding="utf8"
)



# knowledge answer builder
builder = ROOT / "learning/knowledge_answer_builder.py"

builder.write_text(
'''def build_answer(result, question):

    if not result:
        return None

    if isinstance(result,str):
        return result

    if isinstance(result,dict):

        domain=result.get(
            "domain",
            result.get("topic","")
        )

        content=result.get(
            "content",
            result.get("answer","")
        )

        if content:
            if domain:
                return (
                    "תחום: "
                    + str(domain)
                    + "\\n\\n"
                    + str(content)
                )

            return str(content)

    return None
''',
encoding="utf8"
)



# patch runtime
runtime=ROOT/"ima_master_runtime.py"

text=runtime.read_text(encoding="utf8")

if "knowledge_answer_builder" not in text:

    text=text.replace(
        "import ima_brain",
        "import ima_brain\nfrom learning.knowledge_answer_builder import build_answer"
    )

    old='''if brain_answer:

                      result["response"]=brain_answer'''

    new='''if brain_answer:

                      result["response"]=brain_answer

                  else:
                      try:
                          knowledge_answer = build_answer(
                              result.get("knowledge"),
                              message
                          )

                          if knowledge_answer:
                              result["response"]=knowledge_answer

                      except Exception:
                          pass'''

    if old in text:
        text=text.replace(old,new)

runtime.write_text(
    text,
    encoding="utf8"
)



# verify
import py_compile
import importlib

files=[
"ima_master_runtime.py",
"brain_sync.py",
"learning/knowledge_answer_builder.py",
"learning/learning_memory.py"
]

for f in files:
    py_compile.compile(
        f,
        doraise=True
    )


