from pathlib import Path
import shutil
import time
import json

runtime = Path("ima_master_runtime.py")
backup = Path(".ima/backup_knowledge_response")
backup.mkdir(parents=True, exist_ok=True)

shutil.copy2(
    runtime,
    backup / "ima_master_runtime.py"
)

text = runtime.read_text(encoding="utf8")

# הזרקה: אחרי בניית knowledge ולפני fallback של Mom
marker = '''if brain_answer:

                      result["response"]=brain_answer'''

inject = '''if brain_answer:

                      result["response"]=brain_answer

                  else:
                      try:
                          from learning.knowledge_answer_builder import build_answer

                          knowledge_answer = build_answer(
                              result.get("knowledge"),
                              message
                          )

                          if knowledge_answer:
                              result["response"] = knowledge_answer

                      except Exception:
                          pass'''

if "knowledge_answer_builder import build_answer" not in text:
    if marker not in text:
        raise Exception("לא נמצא מקום חיבור knowledge במסלול")

    text = text.replace(marker, inject, 1)

runtime.write_text(
    text,
    encoding="utf8"
)

Path(".ima/knowledge_response.lock").write_text(
    json.dumps({
        "system":"IMA",
        "connection":"Knowledge -> Answer Builder -> Response",
        "state":"CONNECTED",
        "time":time.time()
    }, ensure_ascii=False, indent=2),
    encoding="utf8"
)

print("KNOWLEDGE RESPONSE CONNECTED")
