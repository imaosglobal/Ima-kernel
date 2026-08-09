from pathlib import Path
import shutil
import time
import json

runtime = Path("ima_master_runtime.py")
backup = Path(".ima/backup_knowledge_pipeline_final")

backup.mkdir(parents=True, exist_ok=True)

shutil.copy2(
    runtime,
    backup / "ima_master_runtime.py"
)

text = runtime.read_text(encoding="utf8")

old = '''                  if brain_answer:

                      result["response"]=brain_answer

                  else:

                      memory_hits=conversation_layer.recall(message)'''

new = '''                  if brain_answer:

                      result["response"]=brain_answer

                  else:

                      knowledge_answer=None

                      try:
                          knowledge_result = {
                              "domain":"knowledge",
                              "content": ima_brain.answer(
                                  message,
                                  events
                              )
                          }

                          knowledge_answer = build_answer(
                              knowledge_result,
                              message
                          )

                      except Exception:
                          knowledge_answer=None

                      if knowledge_answer:
                          result["response"]=knowledge_answer

                      else:

                          memory_hits=conversation_layer.recall(message)'''

if old not in text:
    raise Exception("לא נמצא בלוק החיבור. לא שונה כלום.")

text = text.replace(old,new,1)

runtime.write_text(
    text,
    encoding="utf8"
)

Path(".ima/knowledge_pipeline_final.lock").write_text(
    json.dumps({
        "system":"IMA",
        "connection":"Brain -> Knowledge Builder -> Response",
        "state":"CONNECTED",
        "time":time.time()
    },ensure_ascii=False,indent=2),
    encoding="utf8"
)

print("KNOWLEDGE PIPELINE CONNECTED")
