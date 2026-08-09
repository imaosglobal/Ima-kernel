from pathlib import Path
import shutil
import json
import time
import py_compile

runtime = Path("ima_master_runtime.py")

backup = Path(".ima/pipeline_backup")
backup.mkdir(parents=True, exist_ok=True)

shutil.copy2(
    runtime,
    backup / "ima_master_runtime.py"
)

text = runtime.read_text(encoding="utf8")

if "knowledge_answer = build_answer" in text:
    print("Knowledge pipeline already exists")
else:
    marker = 'if brain_answer:'

    pos = text.find(marker)

    if pos == -1:
        raise Exception("brain_answer block not found")

    insert = '''
                      knowledge_answer=None

                      try:
                          knowledge_result = {
                              "domain":"knowledge",
                              "content": brain_answer
                          }

                          knowledge_answer = build_answer(
                              knowledge_result,
                              message
                          )

                      except Exception:
                          knowledge_answer=None

                      if knowledge_answer:
                          result["response"]=knowledge_answer

'''

    text = text[:pos] + insert + text[pos:]

    runtime.write_text(
        text,
        encoding="utf8"
    )

Path(".ima/core_pipeline_repair.lock").write_text(
    json.dumps({
        "system":"IMA",
        "pipeline":"Brain -> Knowledge Builder -> Response",
        "state":"CONNECTED",
        "time":time.time()
    },ensure_ascii=False,indent=2),
    encoding="utf8"
)

py_compile.compile(
    "ima_master_runtime.py",
    doraise=True
)

print("IMA CORE PIPELINE REPAIR COMPLETE")
