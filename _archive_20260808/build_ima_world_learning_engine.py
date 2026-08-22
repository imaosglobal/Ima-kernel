from pathlib import Path
import json
import time
import py_compile
import shutil

IMA = Path(".ima")
LEARNING = Path("learning")

IMA.mkdir(exist_ok=True)
LEARNING.mkdir(exist_ok=True)

runtime = Path("ima_master_runtime.py")
backup = IMA / "backup_before_world_learning_engine.py"

shutil.copy2(runtime, backup)

engine = LEARNING / "world_learning_engine.py"

engine.write_text("""
from pathlib import Path
import json
import time

STORE = Path("learning/world_knowledge_store.json")

def load_store():
    if STORE.exists():
        return json.loads(STORE.read_text(encoding="utf8"))
    return {}

def save_store(data):
    STORE.write_text(
        json.dumps(data,ensure_ascii=False,indent=2),
        encoding="utf8"
    )

def learn_unknown(question):
    store = load_store()

    if question in store:
        return store[question]

    # מקום חיבור עתידי:
    # API / מסמכים / מאגרי ידע / מודלים חיצוניים

    result = {
        "question": question,
        "content": "נדרש מקור ידע חיצוני",
        "source": "expansion_queue",
        "confidence": 0.0,
        "created": time.time()
    }

    store[question] = result
    save_store(store)

    return result
""",encoding="utf8")


# חיבור ל-runtime
text = runtime.read_text(encoding="utf8")

if "from learning.world_learning_engine import learn_unknown" not in text:
    text = text.replace(
        "from learning.knowledge_answer_builder import build_answer",
        """from learning.knowledge_answer_builder import build_answer
from learning.world_learning_engine import learn_unknown"""
    )

# הכנסת הרחבה אחרי שאין brain_answer
old = """if not brain_answer:
                      try:
                          brain_answer=ima_brain.answer(
                              message,
                              events
                          )
                      except Exception:
                          brain_answer=None"""

new = """if not brain_answer:
                      try:
                          brain_answer=ima_brain.answer(
                              message,
                              events
                          )
                      except Exception:
                          brain_answer=None

                  if not brain_answer:
                      try:
                          expansion = learn_unknown(message)
                          brain_answer = (
                              "לא מצאתי ידע קיים. "
                              "הוספתי את השאלה למסלול הרחבת הידע: "
                              + expansion.get("question","")
                          )
                      except Exception:
                          pass"""

if "expansion = learn_unknown" not in text:
    if old not in text:
        raise Exception("לא נמצא אזור חיבור runtime")
    text=text.replace(old,new,1)

runtime.write_text(text,encoding="utf8")

py_compile.compile("ima_master_runtime.py",doraise=True)
py_compile.compile("learning/world_learning_engine.py",doraise=True)


import ima_master_runtime
from learning.world_learning_engine import load_store

m=ima_master_runtime.IMAMaster()

tests=[
    "מה זה חתול",
    "מה הקשר בין מוזיקה ומתמטיקה",
    "איך עובד מוח אנושי"
]

results={}

for q in tests:
    r=m.ask(q)
    results[q]=r.get("response","")[:300]

report={
    "time":time.time(),
    "component":"IMA World Learning Engine",
    "tests":results,
    "store_size":len(load_store())
}

IMA.joinpath("world_learning_engine_report.json").write_text(
    json.dumps(report,ensure_ascii=False,indent=2),
    encoding="utf8"
)

