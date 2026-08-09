from pathlib import Path
import time
import json
import shutil

runtime = Path("ima_master_runtime.py")
backup = Path(".ima/backup_before_knowledge_final")

backup.mkdir(parents=True, exist_ok=True)

if runtime.exists():
    shutil.copy2(
        runtime,
        backup / runtime.name
    )

text = runtime.read_text(encoding="utf8")

if "knowledge_answer_builder" not in text:
    text = text.replace(
        "import ima_brain",
        "import ima_brain\nfrom learning.knowledge_answer_builder import build_answer"
    )

# חיבור שכבת ידע לפני fallback
marker = '''
else:

                      result["response"]=ima_mom.generate_answer(
'''

inject = '''
else:

                      try:
                          knowledge_data = result.get("knowledge_result")

                          if knowledge_data:
                              answer = build_answer(
                                  knowledge_data,
                                  message
                              )

                              if answer:
                                  result["response"] = answer
                                  return result

                      except Exception:
                          pass

                      result["response"]=ima_mom.generate_answer(
'''

if marker in text and "knowledge_result" not in text:
    text = text.replace(marker, inject)

runtime.write_text(
    text,
    encoding="utf8"
)

Path(".ima/knowledge_connection.lock").write_text(
    json.dumps(
        {
            "system":"IMA",
            "layer":"Knowledge->AnswerBuilder->Response",
            "state":"CONNECTED",
            "time":time.time()
        },
        indent=2,
        ensure_ascii=False
    ),
    encoding="utf8"
)

print("KNOWLEDGE FINAL CONNECTION CREATED")
